from Game import Board, LEFT, RIGHT, UP, DOWN, GameOver

import pygame


class SnakeInterface:

    def __init__(self):
        self._running = True
        self._game_over = False
        self._board = Board()
        self._frame_rate = 7
        self._clock = pygame.time.Clock()

    def run(self):
        """Game loop"""
        pygame.init()

        try:
            while self._running:
                self._clock.tick(self._frame_rate)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False

                if not self._game_over:
                    self._time_pass()
        finally:
            pygame.quit()

    def _time_pass(self):
        """Handles passage of time and handles different key presses"""
        # gets whatever key was pressed
        keys = pygame.key.get_pressed()

        # checks for arrow keys and sends the corresponding direction to game logic
        try:
            if keys[pygame.K_LEFT]:
                self._board.run(LEFT)
            elif keys[pygame.K_RIGHT]:
                self._board.run(RIGHT)
            elif keys[pygame.K_UP]:
                self._board.run(UP)
            elif keys[pygame.K_DOWN]:
                self._board.run(DOWN)
            else:
                self._board.run()
        except GameOver:
            self._game_over = True


if __name__ == '__main__':
    SnakeInterface().run()
