# Problema 2.1

#black = 1, white = -1

board = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, -1, 0, 0, 0,
    0, 0, 0, -1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0

]

AVAILABLE_ACTIONS = [
    8, -8, 1, -1, -9, -7, 9, 7
]

def inside_board(pos):
    return -1 < pos < 64

def same_row(i1, i2):
    return i1//8 == i2//8

def is_move_valid(board_state, player_turn, index):

    # can t put a piece on top of another
    if board_state[index] != 0:
        return False

    opponent = - player_turn
    valid = False

    for a in AVAILABLE_ACTIONS:
        pos = index + a
        found_opponent = False

        while inside_board(pos):
            if a == 1 and not same_row(pos - 1, pos): break
            if a == -1 and not same_row(pos + 1, pos): break

            if board_state[pos] == opponent:
                found_opponent = True
            elif board_state[pos] == player_turn and found_opponent:
                valid = True
                break
            else:
                break

            pos += a

    return valid


def get_valid_moves(board_state, player_turn):
    return [i for i in range(64) if is_move_valid(board_state, player_turn, i)]

def apply_move(board_state, player_turn, index):
    pass







###################################
# EURISTICA


def heuristic(board_state):
    pass


###################################
# MINIMAX CU ALFA BETA

def minimax():
    pass


###################################
# TESTARE

















