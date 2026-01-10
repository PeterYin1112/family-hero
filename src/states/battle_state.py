import pygame
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, YELLOW
from src.entities.character import Character
from src.entities.monster import Monster
from src.engines.math_engine import MathEngine
from src.engines.english_engine import EnglishEngine

class BattleState:
    def __init__(self, renderer):
        self.renderer = renderer
        self.manager = None
        self.math_engine = None
        self.english_engine = None

        # Game State
        self.mode = None
        self.char_id = None
        self.character = None
        self.monster = None
        self.current_question = None
        self.options = []
        self.feedback = ""
        self.feedback_timer = 0
        self.consecutive_correct = 0
        self.fever_mode = False
        self.input_text = ""
        self.typing_mode = False

        # Shake effect
        self.shake_timer = 0
        self.shake_offset = (0, 0)

    def enter(self, **kwargs):
        self.mode = kwargs.get("mode")
        self.char_id = kwargs.get("char_id")

        self.math_engine = MathEngine(self.manager.dm)
        self.english_engine = EnglishEngine(self.manager.dm)

        char_data = self.manager.dm.get_character_data(self.char_id)
        level = char_data.get("level", 1)

        self.character = Character(self.char_id, level)
        self.character.equipment = char_data.get("equipment", [])

        self.spawn_monster()
        self.next_question()

        self.consecutive_correct = 0
        self.fever_mode = False
        self.input_text = ""

    def exit(self):
        pass

    def spawn_monster(self):
        level = self.character.level
        is_boss = (level % 10 == 0)
        self.monster = Monster(level, is_boss)

    def next_question(self):
        self.input_text = "" # Reset input
        if self.mode == "math":
            q, a = self.math_engine.generate_question(self.char_id)
            self.current_question = {"text": q, "answer": a}
            self.generate_math_options(a)
            self.typing_mode = False
        else:
            q_data = self.english_engine.generate_question(self.char_id)
            if not q_data:
                 self.current_question = {"text": "No Vocab Found", "answer": ""}
                 return

            self.current_question = q_data

            # Decide mode: Let's default to Select, but maybe allow toggle?
            # For now, let's say Level > 5 enables Typing Mode chance?
            # Or just user toggle. Let's make it random for variety if not specified,
            # OR better, add a toggle button in UI.
            # I will add a toggle button in the UI updates. Default to Select.
            if self.typing_mode:
                self.options = []
            else:
                self.options = self.english_engine.get_options(q_data["answer"], self.char_id)

    def generate_math_options(self, answer):
        # Generate 3 distractors
        # Simple logic: +/- 1, 2, 10, random
        try:
            ans_val = float(answer.split()[0]) # Handle "3 1" remainder case if needed
            if " " in answer:
                 # Remainder handling
                 # Answer is string "3 1"
                 q, r = map(int, answer.split())
                 ans_val = q
            else:
                 ans_val = int(float(answer))
        except:
            ans_val = 0 # Should not happen

        distractors = set()
        while len(distractors) < 3:
            offset = random.choice([-1, 1, -2, 2, -10, 10, random.randint(-5, 5)])
            d = ans_val + offset
            if d != ans_val and d >= 0: # simple constraint
                 # If remainder type, format back
                 if " " in answer:
                      d_r = random.randint(0, 5)
                      distractors.add(f"{int(d)} {d_r}")
                 else:
                      distractors.add(str(int(d)))

        self.options = list(distractors) + [answer]
        random.shuffle(self.options)

    def check_answer(self, user_answer):
        correct_answer = self.current_question["answer"]
        is_correct = (str(user_answer).strip().lower() == str(correct_answer).strip().lower())

        if is_correct:
            self.handle_correct()
        else:
            self.handle_wrong()

        # Prepare next turn after delay
        self.feedback_timer = 60 # 1 second at 60fps

    def handle_correct(self):
        self.feedback = "正確! Correct!"

        # Fever logic
        self.consecutive_correct += 1
        if self.consecutive_correct >= 3:
            self.fever_mode = True

        score_gain = 100
        if self.fever_mode:
            score_gain = int(score_gain * 1.5)
        if self.typing_mode:
            score_gain = int(score_gain * 1.5)

        # Update Data
        self.manager.dm.update_character_data(self.char_id, "score",
            self.manager.dm.get_character_data(self.char_id).get("score", 0) + score_gain)

        # Damage Monster
        self.monster.take_damage(30) # Fixed damage for now

        if self.monster.is_dead():
            self.handle_monster_death()
        else:
            self.next_question()

    def handle_wrong(self):
        self.feedback = "錯誤! Wrong!"
        self.consecutive_correct = 0
        self.fever_mode = False

        # Shake Screen
        self.shake_timer = 20

        # Damage Player
        self.character.take_damage(10)

    def handle_monster_death(self):
        self.character.level += 1
        self.manager.dm.update_character_data(self.char_id, "level", self.character.level)

        if self.monster.is_boss:
            # Drop Item
            drops = ["Ice Wand", "Beetle Helmet", "Magic Cape", "Power Glove"]
            item = random.choice(drops)
            current_eq = self.manager.dm.get_character_data(self.char_id).get("equipment", [])
            if item not in current_eq:
                current_eq.append(item)
                self.manager.dm.update_character_data(self.char_id, "equipment", current_eq)
                self.character.equipment = current_eq
                self.feedback = f"Boss被打敗! 獲得 {item}!"
            else:
                self.feedback = "Boss被打敗!"
        else:
            self.feedback = "怪物被打敗!"

        self.spawn_monster()
        self.next_question()

    def update(self, dt, events):
        self.character.update(dt)
        self.monster.update(dt)

        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.shake_offset = (random.randint(-5, 5), random.randint(-5, 5))
        else:
            self.shake_offset = (0, 0)

        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                self.feedback = ""

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

                    # Back Button
                    if pygame.Rect(10, 10, 80, 40).collidepoint(mouse_pos):
                        self.manager.change_state("hub", char_id=self.char_id)
                        return

                    # Toggle Typing Mode (Only for English)
                    if self.mode == "english":
                         if pygame.Rect(650, 10, 140, 40).collidepoint(mouse_pos):
                              self.typing_mode = not self.typing_mode
                              self.next_question() # Reset question to apply mode
                              return

                    # Options (if not typing mode)
                    if not self.typing_mode and self.options:
                        # Layout: 2x2 grid below character
                        for i, opt in enumerate(self.options):
                            col = i % 2
                            row = i // 2
                            x = 100 + col * 300
                            y = 450 + row * 70
                            if pygame.Rect(x, y, 280, 60).collidepoint(mouse_pos):
                                self.check_answer(opt)

            # Keyboard Input for Typing Mode
            if event.type == pygame.KEYDOWN:
                 if self.typing_mode:
                      if event.key == pygame.K_RETURN:
                           self.check_answer(self.input_text)
                      elif event.key == pygame.K_BACKSPACE:
                           self.input_text = self.input_text[:-1]
                      else:
                           self.input_text += event.unicode

    def draw(self):
        # Apply shake
        surf = self.renderer.screen

        ox, oy = self.shake_offset

        # Background
        surf.fill(WHITE)

        # Draw Entities (offset by shake)
        self.character.rect.x += ox
        self.character.rect.y += oy
        self.character.draw(surf)
        self.character.rect.x -= ox # Reset
        self.character.rect.y -= oy

        self.monster.rect.x += ox
        self.monster.rect.y += oy
        self.monster.draw(surf)
        self.monster.rect.x -= ox
        self.monster.rect.y -= oy

        # Question Display
        q_text = self.current_question["sentence"] if self.mode == "english" else self.current_question["text"]
        self.renderer.draw_text(q_text, 48, SCREEN_WIDTH//2 + ox, 100 + oy, BLACK, center=True)

        if self.mode == "english":
            hint = self.current_question.get("context_zh", "")
            self.renderer.draw_text(hint, 24, SCREEN_WIDTH//2 + ox, 160 + oy, (100, 100, 100), center=True)

            # Typing Mode Toggle
            mode_text = "切換打字" if not self.typing_mode else "切換選擇"
            self.renderer.draw_button(mode_text, 650, 10, 140, 40, (200, 200, 255), (220, 220, 255))

        # Options or Input Box
        if not self.typing_mode and self.options:
            for i, opt in enumerate(self.options):
                col = i % 2
                row = i // 2
                x = 100 + col * 300 + ox
                y = 450 + row * 70 + oy
                self.renderer.draw_button(str(opt), x, y, 280, 60, BLUE, (100, 100, 255))
        elif self.typing_mode:
             # Input Box
             pygame.draw.rect(surf, (240, 240, 240), (200, 450, 400, 60), border_radius=10)
             pygame.draw.rect(surf, BLACK, (200, 450, 400, 60), 2, border_radius=10)
             self.renderer.draw_text(self.input_text + "_", 32, 400, 480, BLACK, center=True)
             self.renderer.draw_text("輸入答案並按 Enter", 16, 400, 520, (100, 100, 100), center=True)

        # HP Bars
        # Player
        pygame.draw.rect(surf, RED, (50, 50, 200, 20))
        p_ratio = self.character.current_hp / self.character.max_hp
        pygame.draw.rect(surf, GREEN, (50, 50, 200 * p_ratio, 20))

        # Monster
        pygame.draw.rect(surf, RED, (550, 50, 200, 20))
        m_ratio = self.monster.current_hp / self.monster.max_hp
        pygame.draw.rect(surf, GREEN, (550, 50, 200 * m_ratio, 20))

        # Feedback
        if self.feedback:
            color = GREEN if "Correct" in self.feedback or "正確" in self.feedback else RED
            self.renderer.draw_text(self.feedback, 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, color, shadow=True)

        # Fever Indicator
        if self.fever_mode:
            self.renderer.draw_text("FEVER 模式!", 32, SCREEN_WIDTH//2, 50, (255, 100, 0), shadow=True)

        # Back Button
        self.renderer.draw_button("退出", 10, 10, 80, 40, (100, 100, 100), (150, 150, 150))
