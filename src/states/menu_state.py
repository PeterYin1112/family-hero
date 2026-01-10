import pygame
from src.constants import CHAR_CONFIG, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, GREEN
from src.entities.character import Character

class MenuState:
    def __init__(self, renderer):
        self.renderer = renderer
        self.manager = None
        self.char_previews = []
        self.setup_previews()

    def setup_previews(self):
        # Create character instances for display
        spacing = SCREEN_WIDTH // 5
        for i, (char_id, config) in enumerate(CHAR_CONFIG.items()):
            char = Character(char_id)
            # Override position for menu
            char.rect.x = spacing * (i + 1) - 30
            char.rect.y = SCREEN_HEIGHT // 2
            self.char_previews.append(char)

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def update(self, dt, events):
        for char in self.char_previews:
            char.update(dt)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    # Check character clicks
                    for char in self.char_previews:
                        if char.rect.collidepoint(mouse_pos):
                            self.manager.change_state("hub", char_id=char.char_id)
                            return

                    # Check Settings button
                    if pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 40).collidepoint(mouse_pos):
                        self.manager.change_state("admin")

    def draw(self):
        self.renderer.screen.fill(WHITE)
        self.renderer.draw_text("家庭英雄任務", 64, SCREEN_WIDTH//2, 100, BLUE, shadow=True)
        self.renderer.draw_text("選擇你的英雄", 32, SCREEN_WIDTH//2, 180, GREEN)

        for char in self.char_previews:
            char.draw(self.renderer.screen)
            # Draw Name
            self.renderer.draw_text(char.config["display_name"], 24, char.rect.centerx, char.rect.bottom + 20, (50, 50, 50))

        # Settings Button
        self.renderer.draw_button("設定", SCREEN_WIDTH - 120, 10, 100, 40, (100, 100, 100), (150, 150, 150))
