"""Obstáculos que caen por la pantalla."""
import random
import pygame

from config import *


class Obstacle:
    def __init__(self):
        size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
        x = random.randint(0, WIDTH - size)
        self.rect = pygame.Rect(x, -size, size, size)
        self.color = random.choice(OBSTACLES_COLORS)
        self.speed = random.randint(2, 7)

    def move(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.y > HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
