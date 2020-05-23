from Game import Board, LEFT, RIGHT, UP, DOWN, GameOver

import pygame


class SnakeInterface:
    # TODO: display board, snake, and food in PyGame and display game over message

    def __init__(self):
        self._running = True
        self._game_over = False
        self._game = Board()
        self._frame_rate = 7
        self._clock = pygame.time.Clock()
        self._surface = None

    def run(self):
        """Game loop"""
        pygame.init()
        self._surface = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)

        try:
            while self._running:
                self._clock.tick(self._frame_rate)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False

                if not self._game_over:
                    self._time_pass()

                self._draw_frame()
        finally:
            pygame.quit()

    def _time_pass(self):
        """Handles passage of time and handles different key presses"""
        # gets whatever key was pressed
        keys = pygame.key.get_pressed()

        # checks for arrow keys and sends the corresponding direction to game logic
        try:
            if keys[pygame.K_LEFT]:
                self._game.run(LEFT)
            elif keys[pygame.K_RIGHT]:
                self._game.run(RIGHT)
            elif keys[pygame.K_UP]:
                self._game.run(UP)
            elif keys[pygame.K_DOWN]:
                self._game.run(DOWN)
            else:
                self._game.run()
        except GameOver:
            self._game_over = True

        self._draw_frame()

    def _draw_frame(self):
        """Draws frame based on game state"""
        self._surface.fill(pygame.Color(255, 255, 255))
        self._draw_board()
        if self._game_over:
            self._display_game_over()
        pygame.display.flip()

    def _draw_board(self):
        """Draws board based on game state"""

    def _display_game_over(self):
        """Displays game over message"""


if __name__ == '__main__':
    SnakeInterface().run()
