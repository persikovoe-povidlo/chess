import constants


def tile_to_coords(row, col):
    return (constants.BOARD_POS_X + col * constants.TILE_SIZE,
            constants.BOARD_POS_Y + row * constants.TILE_SIZE)


def coords_to_tile(x, y):
    return ((x - constants.BOARD_POS_X) // constants.TILE_SIZE,
            (y - constants.BOARD_POS_Y) // constants.TILE_SIZE)
