import pygame
import math
from src.constants import CHAR_CONFIG, RED, GREEN, BLUE, WHITE

class Character:
    def __init__(self, char_id, level=1):
        self.char_id = char_id
        self.config = CHAR_CONFIG[char_id]
        self.level = level
        self.max_hp = 100 + (level * 10)
        self.current_hp = self.max_hp
        self.rect = pygame.Rect(100, 350, 60, 100)
        self.animation_timer = 0
        self.idle_offset = 0
        self.equipment = [] # List of strings describing equipment

    def update(self, dt):
        # Idle animation (bobbing)
        self.animation_timer += dt
        self.idle_offset = math.sin(self.animation_timer * 0.005) * 5

    def draw(self, surface):
        x, y = self.rect.x, self.rect.y + self.idle_offset

        # Procedural Drawing based on theme
        colors = self.config["colors"]
        primary = colors[0]
        secondary = colors[1]

        # Body
        pygame.draw.rect(surface, primary, (x, y + 30, 60, 70), border_radius=5)
        # Head
        pygame.draw.circle(surface, secondary, (x + 30, y + 15), 25)

        # Simple Face
        pygame.draw.circle(surface, WHITE, (x + 20, y + 10), 5)
        pygame.draw.circle(surface, WHITE, (x + 40, y + 10), 5)
        pygame.draw.line(surface, WHITE, (x + 20, y + 25), (x + 40, y + 25), 2)

        # Theme specifics
        if self.config["theme"] == "Ice Princess":
            # Crown
            pygame.draw.polygon(surface, WHITE, [(x+10, y-10), (x+20, y+5), (x+30, y-15), (x+40, y+5), (x+50, y-10)])
        elif self.config["theme"] == "Beetle King":
            # Horns
            pygame.draw.line(surface, secondary, (x+10, y-5), (x+5, y-15), 4)
            pygame.draw.line(surface, secondary, (x+50, y-5), (x+55, y-15), 4)
        elif self.config["theme"] == "Wonder Woman":
            # Tiara
            pygame.draw.polygon(surface, (255, 215, 0), [(x+10, y), (x+30, y+10), (x+50, y)])
        elif self.config["theme"] == "Super Dad":
            # Cape
            pygame.draw.polygon(surface, RED, [(x, y+30), (x+60, y+30), (x+30, y+90)])

        # Equipment (Simple visual representation)
        for item in self.equipment:
            if "Wand" in item:
                pygame.draw.line(surface, (100, 200, 255), (x+60, y+50), (x+80, y+40), 3)
            elif "Helmet" in item:
                pygame.draw.arc(surface, (100, 100, 100), (x+5, y-5, 50, 40), 0, 3.14, 3)

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)
