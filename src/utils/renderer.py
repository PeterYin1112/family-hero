import pygame
from src.constants import FONT_PATH, WHITE, BLACK

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font_large = pygame.font.Font(FONT_PATH, 48)
            self.font_medium = pygame.font.Font(FONT_PATH, 32)
            self.font_small = pygame.font.Font(FONT_PATH, 24)
            self.font_tiny = pygame.font.Font(FONT_PATH, 16)
        except Exception as e:
            print(f"Error loading font: {e}")
            # Fallback to default system font
            self.font_large = pygame.font.SysFont("arial", 48)
            self.font_medium = pygame.font.SysFont("arial", 32)
            self.font_small = pygame.font.SysFont("arial", 24)
            self.font_tiny = pygame.font.SysFont("arial", 16)

    def draw_text(self, text, font_size, x, y, color=WHITE, center=True, shadow=False):
        if font_size >= 48:
            font = self.font_large
        elif font_size >= 32:
            font = self.font_medium
        elif font_size >= 24:
            font = self.font_small
        else:
            font = self.font_tiny

        if shadow:
            shadow_surface = font.render(text, True, BLACK)
            shadow_rect = shadow_surface.get_rect()
            if center:
                shadow_rect.center = (x + 2, y + 2)
            else:
                shadow_rect.topleft = (x + 2, y + 2)
            self.screen.blit(shadow_surface, shadow_rect)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_button(self, text, x, y, w, h, base_color, hover_color, action=None):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        rect = pygame.Rect(x, y, w, h)
        is_hovered = rect.collidepoint(mouse_pos)

        color = hover_color if is_hovered else base_color

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)

        self.draw_text(text, 24, x + w//2, y + h//2, WHITE, center=True)

        if is_hovered and click[0] == 1 and action:
            return True
        return False
