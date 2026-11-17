"""Lógica y estado de la partida."""
import pygame

from config import *
from player import Player
from obstacle import Obstacle


class Game:
    def __init__(self):
        self.player1 = Player(375, 530)
        self.player2 = Player(100, 100, PLAYER_COLOR2)
        self.players = [self.player1, self.player2]
        self.high_score = 0          # Reto 9: sobrevive a los reinicios
        self.reset()

    def reset(self):
        """Reto 5: nueva partida (el récord se conserva)."""
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.survival_ms = 0         # Reto 6
        self.spawn_timer = 0
        for p in self.players:
            p.reset()

    def spawn_delay(self):
        """Reto 7: -50 ms cada 10 puntos, mínimo 150 ms."""
        delay = SPAWN_OBSTACLE_DELAY - SPAWN_DELAY_STEP * (self.score // POINTS_PER_LEVEL)
        return max(MIN_SPAWN_DELAY, delay)

    #---------- Eventos ------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE and not self.game_over:      # Reto 4
            self.paused = not self.paused
        elif event.key == pygame.K_r and self.game_over:             # Reto 5
            self.reset()
        elif not self.paused and not self.game_over:                 # Reto 8
            if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS) or event.unicode == "+":
                self.player1.change_speed(1)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) or event.unicode == "-":
                self.player1.change_speed(-1)

    #------- actualización ---------------
    def update(self, dt):
        if self.game_over or self.paused:
            return

        self.survival_ms += dt
        for p in self.players:
            p.update_invulnerability(dt)

        self._spawn_obstacles(dt)
        self._update_obstacles()

        if self.score > self.high_score:
            self.high_score = self.score

        #solo se mueven los jugadores que siguen vivos
        if self.player1.alive:
            self.player1.moveArrows()
        if self.player2.alive:
            self.player2.moveWASD()

        #reto 10
        if not any(p.alive for p in self.players):
            self.game_over = True

    def _spawn_obstacles(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay():
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0

    def _update_obstacles(self):
        visible = []
        for obstacle in self.obstacles:
            obstacle.move()
            # reto 3 / 10
            for p in self.players:
                if p.alive and not p.invulnerable and p.rect.colliderect(obstacle.rect):
                    p.hit()
            if obstacle.is_off_screen():
                self.score += 1
            else:
                visible.append(obstacle)
        self.obstacles = visible
