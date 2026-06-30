import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:

    def __init__(self):
        pygame.init()

        self.fullscreen = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = game.board
        dragger = game.dragger

        while True:

            screen.fill((0, 0, 0))

            # Draw board
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # -----------------------------
                # Mouse button down
                # -----------------------------
                if event.type == pygame.MOUSEBUTTONDOWN:

                    dragger.update_mouse(event.pos)

                    clicked_row = (dragger.mouseY - BOARD_Y) // SQSIZE
                    clicked_col = (dragger.mouseX - BOARD_X) // SQSIZE

                    if not (0 <= clicked_row < ROWS and 0 <= clicked_col < COLS):
                        continue

                    if board.squares[clicked_row][clicked_col].has_piece():

                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:

                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)

                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                # -----------------------------
                # Mouse movement
                # -----------------------------
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = (event.pos[1] - BOARD_Y) // SQSIZE
                    motion_col = (event.pos[0] - BOARD_X) // SQSIZE

                    if 0 <= motion_row < ROWS and 0 <= motion_col < COLS:
                        game.set_hover(motion_row, motion_col)
                    else:
                        game.hovered_sqr = None

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                # -----------------------------
                # Mouse released
                # -----------------------------
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        released_row = (dragger.mouseY - BOARD_Y) // SQSIZE
                        released_col = (dragger.mouseX - BOARD_X) // SQSIZE

                        if 0 <= released_row < ROWS and 0 <= released_col < COLS:

                            initial = Square(
                                dragger.initial_row,
                                dragger.initial_col
                            )

                            final = Square(
                                released_row,
                                released_col
                            )

                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):

                                captured = board.squares[
                                    released_row
                                ][released_col].has_piece()

                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)

                                game.play_sound(captured)

                                game.next_turn()

                                # AI move
                                if game.next_player == "black":
                                    game.ai_move()

                        dragger.undrag_piece()

                # -----------------------------
                # Keyboard
                # -----------------------------
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_t:
                        game.change_theme()

                    elif event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = game.board
                        dragger = game.dragger

                # -----------------------------
                # Quit
                # -----------------------------
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()