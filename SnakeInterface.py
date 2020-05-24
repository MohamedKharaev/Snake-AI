from Game import Board, LEFT, RIGHT, UP, DOWN, GameOver

import pygame


class SnakeInterface:
    # TODO: draw borders?

    def __init__(self):
        self._running = True
        self._game_over = False
        self._game_over_message = ""
        self._no_keys_pressed = True
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
                self._no_keys_pressed = True

                # handles various events in PyGame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    elif event.type == pygame.KEYDOWN and not self._game_over:
                        self._no_keys_pressed = False
                        self._handle_keys()

                # snake moves forward if no keys are pressed
                if self._no_keys_pressed:
                    try:
                        if not self._game_over:
                            self._game.run()
                    except GameOver as g:
                        # this is how interface knows when to stop
                        self._game_over = True
                        self._game_over_message = str(g)

                self._draw_frame()
        finally:
            pygame.quit()

    def _handle_keys(self):
        """Handles key presses"""
        # gets whatever key was pressed
        keys = pygame.key.get_pressed()

        try:
            if keys[pygame.K_LEFT]:
                self._game.run(UP)
            elif keys[pygame.K_RIGHT]:
                self._game.run(DOWN)
            elif keys[pygame.K_UP]:
                self._game.run(LEFT)
            elif keys[pygame.K_DOWN]:
                self._game.run(RIGHT)
        except GameOver as g:
            self._game_over = True
            self._game_over_message = str(g)

    def _draw_frame(self):
        """Draws frame based on game state"""
        self._surface.fill(pygame.Color(255, 255, 255))
        self._draw_board()
        if self._game_over:
            self._display_game_over()
        pygame.display.flip()

    def _draw_board(self):
        """Draws board based on game state"""
        width = self._surface.get_width()
        height = self._surface.get_height()
        new_width = .05 * width
        new_height = .05 * height
        x_ratio = .35
        y_ratio = .1

        for row in self._game.board:
            for col in row:
                new_x = x_ratio * width
                new_y = y_ratio * height

                # draws green square for snake tiles and red square for food tiles
                if col.foodTile:
                    pygame.draw.rect(self._surface, (255, 0, 0), (new_x, new_y, new_width, new_height), 0)
                elif col.snakeTile:
                    pygame.draw.rect(self._surface, (0, 255, 0), (new_x, new_y, new_width, new_height), 0)

                y_ratio += .05

            x_ratio += .05
            y_ratio = .1

    def _display_game_over(self):
        """Displays game over message"""
        width = self._surface.get_width()
        height = self._surface.get_height()
        fontsize = int(.1 * width)
        x_ratio = .2
        y_ratio = .75
        new_x = x_ratio * width
        new_y = y_ratio * height
        font = pygame.font.SysFont("comicsansms", fontsize)
        game_over_label = font.render(self._game_over_message, 1, (0, 0, 0))
        self._surface.blit(game_over_label, (new_x, new_y))


if __name__ == '__main__':
    SnakeInterface().run()