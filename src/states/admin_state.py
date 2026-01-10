import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, GREEN, RED, DARK_GREY

class AdminState:
    def __init__(self, renderer):
        self.renderer = renderer
        self.manager = None
        self.mode = "math" # math, vocab

        # Vocab Management State
        self.vocab_category = "animals" # default category
        self.page = 0
        self.items_per_page = 5
        self.input_mode = None # "add_en", "add_zh", "add_type"
        self.new_word = {"en": "", "zh": "", "type": "noun"}

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

                    # Back Button
                    if pygame.Rect(10, 10, 80, 40).collidepoint(mouse_pos):
                        self.manager.change_state("menu")
                        return

                    # Tabs
                    if pygame.Rect(100, 10, 150, 40).collidepoint(mouse_pos):
                        self.mode = "math"
                    if pygame.Rect(260, 10, 150, 40).collidepoint(mouse_pos):
                        self.mode = "vocab"

                    if self.mode == "math":
                        self.handle_math_clicks(mouse_pos)
                    else:
                        self.handle_vocab_clicks(mouse_pos)

            if event.type == pygame.KEYDOWN and self.mode == "vocab" and self.input_mode:
                 self.handle_vocab_input(event)

    def handle_math_clicks(self, pos):
        # Daughter Add Weight
        if pygame.Rect(50, 100, 300, 40).collidepoint(pos):
             settings = self.manager.dm.get_settings()
             w = settings["math_weights"]["daughter"]
             w["add"] = (w["add"] + 10) % 110
             self.manager.dm.update_settings("math_weights", "daughter", w)

        # Daughter Max Range
        if pygame.Rect(50, 160, 300, 40).collidepoint(pos):
             settings = self.manager.dm.get_settings()
             r = settings["math_ranges"]["daughter"]
             if r["max"] == 10: r["max"] = 20
             elif r["max"] == 20: r["max"] = 50
             else: r["max"] = 10
             self.manager.dm.update_settings("math_ranges", "daughter", r)

        # Son/Dad Settings - Toggle Weights
        # We need buttons for each type: add_2d, sub_2d, add_3d, sub_3d, mult_2x1, mult_2x2, div
        types = ["add_2d", "sub_2d", "add_3d", "sub_3d", "mult_2x1", "mult_2x2", "div"]
        for i, t in enumerate(types):
            col = i % 2
            row = i // 2
            x = 400 + col * 180
            y = 100 + row * 60
            if pygame.Rect(x, y, 160, 40).collidepoint(pos):
                settings = self.manager.dm.get_settings()
                w = settings["math_weights"]["son_dad"]
                w[t] = (w.get(t, 0) + 10) % 110 # Increment by 10, wrap at 100 (ish)
                self.manager.dm.update_settings("math_weights", "son_dad", w)

    def handle_vocab_clicks(self, pos):
        settings = self.manager.dm.get_settings()
        vocab = settings["vocab"]
        categories = list(vocab.keys())

        # Category Cycling
        if pygame.Rect(50, 60, 200, 40).collidepoint(pos):
             curr_idx = categories.index(self.vocab_category)
             self.vocab_category = categories[(curr_idx + 1) % len(categories)]
             self.page = 0

        # Add Word Button
        if pygame.Rect(300, 60, 100, 40).collidepoint(pos):
             self.input_mode = "add_en"
             self.new_word = {"en": "", "zh": "", "type": "noun"}

        # Delete/Mark Focus Logic for list items
        current_list = vocab[self.vocab_category]
        start_idx = self.page * self.items_per_page
        for i in range(self.items_per_page):
            idx = start_idx + i
            if idx >= len(current_list): break

            y_base = 150 + i * 50
            # Delete Button (Right side)
            if pygame.Rect(650, y_base, 60, 30).collidepoint(pos):
                 del current_list[idx]
                 self.manager.dm.update_settings("vocab", self.vocab_category, current_list)
                 return

            # Toggle Focus (Only for Brother's focus list really, but generic here)
            # Or "Mark Focus" adds to Brother's list?
            # Prompt says: "Mark Focus Words: Mark specific words as 'High Priority' so they appear more often."
            # Implementation: Add/Remove from "brother_focus" list if not there.
            if pygame.Rect(550, y_base, 80, 30).collidepoint(pos):
                 word = current_list[idx]
                 focus_list = vocab.get("brother_focus", [])
                 # Check if exists by EN key
                 exists = any(w["en"] == word["en"] for w in focus_list)
                 if exists:
                      focus_list = [w for w in focus_list if w["en"] != word["en"]]
                 else:
                      focus_list.append(word)
                 self.manager.dm.update_settings("vocab", "brother_focus", focus_list)
                 return

    def handle_vocab_input(self, event):
        if event.key == pygame.K_RETURN:
            if self.input_mode == "add_en":
                self.input_mode = "add_zh"
            elif self.input_mode == "add_zh":
                self.input_mode = "add_type"
            elif self.input_mode == "add_type":
                # Save
                settings = self.manager.dm.get_settings()
                vocab_list = settings["vocab"][self.vocab_category]
                vocab_list.append(self.new_word)
                self.manager.dm.update_settings("vocab", self.vocab_category, vocab_list)
                self.input_mode = None
        elif event.key == pygame.K_BACKSPACE:
             if self.input_mode == "add_en": self.new_word["en"] = self.new_word["en"][:-1]
             elif self.input_mode == "add_zh": self.new_word["zh"] = self.new_word["zh"][:-1]
             elif self.input_mode == "add_type": self.new_word["type"] = self.new_word["type"][:-1]
        else:
             char = event.unicode
             if self.input_mode == "add_en": self.new_word["en"] += char
             elif self.input_mode == "add_zh":
                 # Basic support for typing, though Chinese IME won't work easily in Pygame directly without system IME support
                 # We'll assume user pastes or types simple things, or this is a limitation.
                 # For the purpose of this task, we assume English typing or simulated input.
                 self.new_word["zh"] += char
             elif self.input_mode == "add_type": self.new_word["type"] += char

    def draw(self):
        self.renderer.screen.fill(WHITE)

        # Back Button
        self.renderer.draw_button("返回", 10, 10, 80, 40, (100, 100, 100), (150, 150, 150))

        # Tabs
        color_math = BLUE if self.mode == "math" else (200, 200, 200)
        color_vocab = GREEN if self.mode == "vocab" else (200, 200, 200)
        self.renderer.draw_button("數學設定", 100, 10, 150, 40, color_math, color_math)
        self.renderer.draw_button("單字管理", 260, 10, 150, 40, color_vocab, color_vocab)

        if self.mode == "math":
            self.draw_math_settings()
        else:
            self.draw_vocab_settings()

    def draw_math_settings(self):
        settings = self.manager.dm.get_settings()

        self.renderer.draw_text("女兒 (Sister) 設定:", 32, 200, 80, BLACK)

        w_add = settings["math_weights"]["daughter"]["add"]
        self.renderer.draw_button(f"加法權重: {w_add}", 50, 100, 300, 40, BLUE, (100, 100, 255))

        max_range = settings["math_ranges"]["daughter"]["max"]
        self.renderer.draw_button(f"最大數值範圍: {max_range}", 50, 160, 300, 40, BLUE, (100, 100, 255))

        # Son/Dad Settings
        self.renderer.draw_text("兒子/爸爸 (Son/Dad) 設定:", 32, 580, 80, BLACK)

        types = ["add_2d", "sub_2d", "add_3d", "sub_3d", "mult_2x1", "mult_2x2", "div"]
        labels = {
            "add_2d": "2位加法", "sub_2d": "2位減法",
            "add_3d": "3位加法", "sub_3d": "3位減法",
            "mult_2x1": "乘法 2x1", "mult_2x2": "乘法 2x2",
            "div": "除法"
        }

        for i, t in enumerate(types):
            col = i % 2
            row = i // 2
            x = 400 + col * 180
            y = 100 + row * 60

            weight = settings["math_weights"]["son_dad"].get(t, 0)
            text = f"{labels[t]}: {weight}"
            self.renderer.draw_button(text, x, y, 160, 40, GREEN, (100, 255, 100))

    def draw_vocab_settings(self):
        settings = self.manager.dm.get_settings()
        vocab = settings["vocab"]

        # Category Selector
        self.renderer.draw_button(f"類別: {self.vocab_category}", 50, 60, 200, 40, GREEN, (100, 255, 100))
        self.renderer.draw_button("新增單字", 300, 60, 100, 40, BLUE, (100, 100, 255))

        if self.input_mode:
             self.renderer.draw_text(f"EN: {self.new_word['en']} | ZH: {self.new_word['zh']} | Type: {self.new_word['type']}",
                                     24, SCREEN_WIDTH//2, 120, RED)
             self.renderer.draw_text("Press Enter to Next/Save", 16, SCREEN_WIDTH//2, 140, DARK_GREY)

        # List Items
        current_list = vocab.get(self.vocab_category, [])
        start_idx = self.page * self.items_per_page

        for i in range(self.items_per_page):
            idx = start_idx + i
            if idx >= len(current_list): break

            word = current_list[idx]
            y = 150 + i * 50

            # Check if focus
            is_focus = any(w["en"] == word["en"] for w in vocab.get("brother_focus", []))
            color = RED if is_focus else BLACK

            text = f"{word['en']} ({word['zh']})"
            self.renderer.draw_text(text, 24, 100, y + 15, color, center=False)

            # Buttons
            focus_text = "取消重點" if is_focus else "設為重點"
            self.renderer.draw_button(focus_text, 550, y, 80, 30, (200, 200, 100), (255, 255, 100))
            self.renderer.draw_button("刪除", 650, y, 60, 30, (200, 100, 100), (255, 100, 100))
