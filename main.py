import pygame

from classes.buttons import UndoButton
from classes.move import Move
from classes.pieces import Pawn, Bishop, Rook, Queen, Knight, King
from classes.board import Board
from functions import tile_to_coords, coords_to_tile
import constants


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    running = True
    board = Board(screen)
    buttons = []
    buttons.append(
        UndoButton(board, constants.BOARD_POS_X - constants.TILE_SIZE, constants.BOARD_POS_Y + constants.TILE_SIZE * 4,
                   constants.TILE_SIZE, constants.TILE_SIZE // 2, 'gray'))
    for i in range(8):
        board.place_piece(Pawn(board, 1, i, 'black'))
        board.place_piece(Pawn(board, 6, i, 'white'))

    board.place_piece(Bishop(board, 7, 2, 'white'))
    board.place_piece(Bishop(board, 7, 5, 'white'))
    board.place_piece(Rook(board, 7, 0, 'white'))
    board.place_piece(Rook(board, 7, 7, 'white'))
    board.place_piece(Queen(board, 7, 3, 'white'))
    board.place_piece(King(board, 7, 4, 'white'))
    board.place_piece(Knight(board, 7, 1, 'white'))
    board.place_piece(Knight(board, 7, 6, 'white'))

    board.place_piece(Bishop(board, 0, 2, 'black'))
    board.place_piece(Bishop(board, 0, 5, 'black'))
    board.place_piece(Rook(board, 0, 0, 'black'))
    board.place_piece(Rook(board, 0, 7, 'black'))
    board.place_piece(Queen(board, 0, 3, 'black'))
    board.place_piece(King(board, 0, 4, 'black'))
    board.place_piece(Knight(board, 0, 1, 'black'))
    board.place_piece(Knight(board, 0, 6, 'black'))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for row in board.tiles:
                        for tile in row:
                            if tile:
                                if tile.rect.collidepoint(event.pos):
                                    if tile.color == board.turn:
                                        board.dragged_piece = tile
                        for button in buttons:
                            if button.rect.collidepoint(event.pos) and not button.pressed:
                                button.press()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if board.dragged_piece:
                        col, row = coords_to_tile(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        if (board.dragged_piece.can_move(row, col) and not (
                                board.dragged_piece.row == row and board.dragged_piece.col == col) and (
                                0 <= row < constants.BOARD_SIZE and 0 <= col < constants.BOARD_SIZE) and (
                                board.tiles[row][col].color != board.dragged_piece.color if board.tiles[row][
                                    col] else True)):
                            board.last_move = Move(board.dragged_piece.row, board.dragged_piece.col, row, col,
                                                   board.tiles[row][col])
                            board.tiles[board.dragged_piece.row][board.dragged_piece.col] = None
                            board.dragged_piece.row = row
                            board.dragged_piece.col = col
                            board.tiles[row][col] = board.dragged_piece
                            board.dragged_piece.rect.topleft = (
                                tile_to_coords(board.dragged_piece.row, board.dragged_piece.col))
                            board.dragged_piece = None
                            if board.turn == 'white':
                                board.turn = 'black'
                            else:
                                board.turn = 'white'
                        else:
                            board.dragged_piece.rect.topleft = (
                                tile_to_coords(board.dragged_piece.row, board.dragged_piece.col))
                            board.dragged_piece = None
                    for button in buttons:
                        button.release()

            if event.type == pygame.MOUSEMOTION:
                if board.dragged_piece:
                    board.dragged_piece.rect.center = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 50, 50))
        board.draw()
        for button in buttons:
            button.draw(screen)
        board.draw_pieces()
        pygame.display.flip()

        clock.tick(60)


pygame.quit()

if __name__ == '__main__':
    main()
