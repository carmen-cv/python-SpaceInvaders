"""Interfaz: puntuaciones, tiempo, vidas y mensajes."""
import pygame

from config import *


class Text:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

    def _text(self, surface, text, color, pos, right=False):
        img = self.font.render(text, True, color)
        rect = img.get_rect(topright=pos) if right else img.get_rect(topleft=pos)
        surface.blit(img, rect)

    def _centered(self, surface, text, font, color, y_offset=0):
        img = font.render(text, True, color)
        surface.blit(img, (WIDTH // 2 - img.get_width() // 2,
                           HEIGHT // 2 - img.get_height() // 2 + y_offset))

    def draw(self, surface, game):
        #puntuación, récord, tiempo, velocidad
        self._text(surface, f"Score: {game.score}", WHITE, (10, 10))
        self._text(surface, f"Record: {game.high_score}", GOLD, (10, 40))
        self._text(surface, f"Tiempo: {int(game.survival_ms // 1000)} s", WHITE, (10, 70))
        self._text(surface, f"Velocidad J1: {game.player1.speed}", GRAY, (10, 100))

        #vidas de cada jugador
        self._text(surface, f"J1 vidas: {game.player1.lives}", game.player1.color,
                   (WIDTH - 10, 10), right=True)
        self._text(surface, f"J2 vidas: {game.player2.lives}", game.player2.color,
                   (WIDTH - 10, 40), right=True)

        if game.paused:
            self._centered(surface, "PAUSE", self.big_font, WHITE)
        if game.game_over:
            self._centered(surface, "Game Over", self.big_font, RED)
            self._centered(surface, "Pulsa R para reiniciar", self.font, WHITE, 50)
