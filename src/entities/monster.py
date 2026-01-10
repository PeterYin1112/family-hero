import pygame
import random
import math
from src.constants import RED, DARK_GREY, YELLOW

class Monster:
    def __init__(self, level, is_boss=False):
        self.level = level
        self.is_boss = is_boss
        self.max_hp = (level * 20) if not is_boss else (level * 50)
        self.current_hp = self.max_hp

        # Position on the right side
        self.rect = pygame.Rect(600, 320, 100, 100) if not is_boss else pygame.Rect(550, 250, 150, 150)

        # Appearance randomization
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.shape_type = random.choice(["rect", "circle", "poly"])
        self.animation_timer = 0
        self.float_offset = 0

    def update(self, dt):
        self.animation_timer += dt
        self.float_offset = math.cos(self.animation_timer * 0.003) * 8

    def draw(self, surface):
        x, y = self.rect.x, self.rect.y + self.float_offset
        w, h = self.rect.width, self.rect.height

        if self.shape_type == "rect":
            pygame.draw.rect(surface, self.color, (x, y, w, h), border_radius=10)
        elif self.shape_type == "circle":
            pygame.draw.circle(surface, self.color, (x + w//2, y + h//2), w//2)
        elif self.shape_type == "poly":
            points = [(x + w//2, y), (x + w, y + h), (x, y + h)]
            pygame.draw.polygon(surface, self.color, points)

        # Boss indicator
        if self.is_boss:
             pygame.draw.circle(surface, RED, (x + w//2, y + h//2), w//2 + 5, 2)
             # Crown
             pygame.draw.polygon(surface, YELLOW, [(x+w//4, y), (x+w//2, y-20), (x+3*w//4, y)])

        # Eyes (Angry)
        eye_y = y + h//3
        pygame.draw.line(surface, DARK_GREY, (x + w//3, eye_y), (x + w//3 + 10, eye_y + 5), 3)
        pygame.draw.line(surface, DARK_GREY, (x + 2*w//3, eye_y), (x + 2*w//3 - 10, eye_y + 5), 3)

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)

    def is_dead(self):
        return self.current_hp <= 0
