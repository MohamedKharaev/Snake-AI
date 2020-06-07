from Game import Board, BOARD_SIZE, LEFT, RIGHT, UP, DOWN, GameOver

import pygame


class SnakeInterface:
    # TODO: draw borders?

    def __init__(self):
        self._running = True
        self._game_over = False
        self._game_over_message = ""
        self._no_keys_pressed = True
        self._game = Board()
        # self._frame_rate = 7 Perhaps we do not need this since we are using clock ticks?
        self._clock = pygame.time.Clock()

        self._surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

    def run(self):
        """Game loop"""
        pygame.init()
        #self._surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

        try:
            while self._running:
                self._clock.tick(2)
                self._no_keys_pressed = True

                # handles various events in PyGame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    elif event.type == pygame.KEYDOWN and not self._game_over:
                        self._no_keys_pressed = False
                        self._handle_keys(event)

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

    def _handle_keys(self, event):
        """Handles key presses"""
        # gets whatever key was pressed
        #keys = pygame.key.get_pressed()

        try:
            if event.key == pygame.K_LEFT:
                self._game.run(LEFT)
            elif event.key == pygame.K_RIGHT:
                self._game.run(RIGHT)
            elif event.key == pygame.K_UP:
                self._game.run(UP)
            elif event.key == pygame.K_DOWN:
                self._game.run(DOWN)
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
        block_size = self._surface.get_width() / BOARD_SIZE - 5
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(x * (block_size + 1), y * (block_size + 1), block_size, block_size)
                if self._game.board[y][x].foodTile:
                    pygame.draw.rect(self._surface, (255, 0, 0), rect)
                elif self._game.board[y][x].snakeTile:
                    pygame.draw.rect(self._surface, (0, 255, 0), rect)
                else:
                    pygame.draw.rect(self._surface, (0, 0, 0), rect)

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
        self._surface.blit(game_over_label, (int(new_x), int(new_y)))


if __name__ == '__main__':
    SnakeInterface().run()
