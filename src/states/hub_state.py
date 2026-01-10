import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, GREEN, CHAR_CONFIG
from src.entities.character import Character

class HubState:
    def __init__(self, renderer):
        self.renderer = renderer
        self.manager = None
        self.char_id = None
        self.character = None
        self.char_data = None

    def enter(self, **kwargs):
        self.char_id = kwargs.get("char_id")
        self.char_data = self.manager.dm.get_character_data(self.char_id)

        # Load character status
        level = self.char_data.get("level", 1)
        self.character = Character(self.char_id, level)
        self.character.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.character.equipment = self.char_data.get("equipment", [])

    def exit(self):
        pass

    def update(self, dt, events):
        self.character.update(dt)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

                    # Math Mode Button
                    if self.renderer.draw_button("數學挑戰", 400, 200, 300, 60, BLUE, (100, 100, 255), action=True):
                        self.manager.change_state("battle", mode="math", char_id=self.char_id)
                        return

                    # English Mode Button
                    if self.renderer.draw_button("英文挑戰", 400, 300, 300, 60, GREEN, (100, 255, 100), action=True):
                         self.manager.change_state("battle", mode="english", char_id=self.char_id)
                         return

                    # Back Button
                    if self.renderer.draw_button("返回", 20, 20, 100, 40, (100, 100, 100), (150, 150, 150), action=True):
                        self.manager.change_state("menu")
                        return

    def draw(self):
        self.renderer.screen.fill(WHITE)

        # Draw Character
        self.character.draw(self.renderer.screen)

        # Stats
        name = CHAR_CONFIG[self.char_id]["display_name"]
        level = self.char_data.get("level", 1)
        score = self.char_data.get("score", 0)

        self.renderer.draw_text(f"{name}", 48, SCREEN_WIDTH // 4, 150, BLACK)
        self.renderer.draw_text(f"等級 (Level): {level}", 32, SCREEN_WIDTH // 4, 450, BLACK)
        self.renderer.draw_text(f"分數 (Score): {score}", 32, SCREEN_WIDTH // 4, 500, BLACK)

        self.renderer.draw_button("數學挑戰", 400, 200, 300, 60, BLUE, (100, 100, 255))
        self.renderer.draw_button("英文挑戰", 400, 300, 300, 60, GREEN, (100, 255, 100))
        self.renderer.draw_button("返回", 20, 20, 100, 40, (100, 100, 100), (150, 150, 150))
