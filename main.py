"""Punto de entrada del juego."""
import pygame

from config import *
from game import Game
from text import Text


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Player Game")
    clock = pygame.time.Clock()

    game = Game()
    text = Text()

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.update(dt)

        screen.fill(BACKGROUND_COLOR)
        for obstacle in game.obstacles:
            obstacle.draw(screen)
        for player in game.players:
            player.draw(screen)
        text.draw(screen, game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
