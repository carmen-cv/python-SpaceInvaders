"""Jugador: movimiento, límites, velocidad y vidas."""
import pygame

from config import *


class Player:
    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = speed
        self.start_pos = (x, y)
        self.start_speed = speed
        self.lives = PLAYER_LIVES
        self.invulnerable_ms = 0

    #-------estado-----
    def reset(self):
        """Posición, velocidad y vidas iniciales."""
        self.rect.topleft = self.start_pos
        self.speed = self.start_speed
        self.lives = PLAYER_LIVES
        self.invulnerable_ms = 0

    @property
    def alive(self):
        return self.lives > 0

    @property
    def invulnerable(self):
        return self.invulnerable_ms > 0

    #----reto10----
    def hit(self):
        """Pierde una vida y activa la invulnerabilidad."""
        self.lives -= 1
        self.invulnerable_ms = INVULNERABILITY_MS

    def update_invulnerability(self, dt):
        if self.invulnerable_ms > 0:
            self.invulnerable_ms = max(0, self.invulnerable_ms - dt)

    #---- movimiento--------
    def change_speed(self, amount):
        self.speed = max(MIN_PLAYER_SPEED, min(MAX_PLAYER_SPEED, self.speed + amount))

    def keep_inside_screen(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def moveArrows(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.keep_inside_screen()

    def moveWASD(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        self.keep_inside_screen()

    def draw(self, surface):
        if not self.alive:
            return  #jugador sin vidas desaparece
        #parpadea mientras es invulnerable
        if self.invulnerable and (self.invulnerable_ms // BLINK_MS) % 2 == 0:
            return
        pygame.draw.rect(surface, self.color, self.rect)
