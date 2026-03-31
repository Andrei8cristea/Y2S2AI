# Problema 2.1
import math

from itertools import product

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

def is_move_valid(board_state, player, index):

    # can't put a piece on top of another
    if board_state[index] != 0:
        return False

    opponent = - player
    valid = False

    for a in AVAILABLE_ACTIONS:
        pos = index + a
        found_opponent = False

        while inside_board(pos):
            if a == 1 and not same_row(pos - 1, pos): break
            if a == -1 and not same_row(pos + 1, pos): break

            if board_state[pos] == opponent:
                found_opponent = True
            elif board_state[pos] == player and found_opponent:
                valid = True
                break
            else:
                break

            pos += a

    return valid


def get_valid_moves(board_state, player):
    return [i for i in range(64) if is_move_valid(board_state, player, i)]

def apply_move(board_state, player, index):
    new_board = board_state[:]
    new_board[index] = player
    opponent = - player

    for a in AVAILABLE_ACTIONS:
        pos = index + a
        pieces_to_flip =[]

        while inside_board(pos):
            if a == 1 and not same_row(pos - 1, pos): break
            if a == -1 and not same_row(pos + 1, pos): break

            if new_board[pos] == opponent:
                pieces_to_flip.append(pos)

            elif new_board[pos] == player:
                for p in pieces_to_flip:
                    new_board[p] = player
                break

            else:
                break

            pos += a

    return new_board





###################################
# EURISTICA


def heuristic(board_state):

    black = board_state.count(1)
    white = board_state.count(-1)


    mob_black = len(get_valid_moves(board_state, 1))
    mob_white = len(get_valid_moves(board_state, -1))


    corners = [0, 7, 56, 63]
    corner_black = sum(1 for c in corners if board_state[c] == 1)
    corner_white = sum(1 for c in corners if board_state[c] == -1)

    return (black - white) + 5 * (mob_black - mob_white) + 25 * (corner_black - corner_white)


###################################
# MINIMAX CU ALFA BETA

def minimax(board_state,alpha,beta,depth,player):
    moves = get_valid_moves(board_state, player)
    if depth == 0 or not moves:
        return heuristic(board_state), None

    best_move = None

    if player == 1: #MAX (Negru)
        max_eval = -math.inf
        for move in moves:
            new_board = apply_move(board_state, player, move)
            eval, _ = minimax(new_board,alpha, beta,depth-1,-player)
            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha,eval)
            if beta <= alpha:
                break


        return max_eval, best_move

    else: #MIN (Alb)
        min_eval = math.inf
        for move in moves:
            new_board = apply_move(board_state, player, move)
            eval, _ = minimax(new_board,alpha, beta,depth-1,-player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta,eval)
            if beta <= alpha:
                break

        return min_eval, best_move

print("TEST 1 PROBLEMA 1:")
score, move = minimax(board, -math.inf, math.inf, 3, 1)
print("Best move for black:", move)

print("TEST 2 PROBLEMA 1:")

new_board = apply_move(board, 1, 19)
score, move = minimax(new_board, -math.inf, math.inf, 3, -1)
print("Best move for white:", move)

print("TEST 3 PROBLEMA 1:")

test_board = [1 if i % 2 == 0 else -1 for i in range(64)]
score, move = minimax(test_board, -math.inf, math.inf, 3, 1)
print("Best move for black:", move)


###################################
########    Problema 2.2    #######
###################################

### EVAL ###

def evaluation(score_me, score_opp):
    free_bacon = 1 + max(score_opp // 10, score_opp % 10)
    danger = score_opp / 100
    return (score_me - score_opp) + 0.3 * free_bacon - 0.5 * danger


### HOG RULES ###

from itertools import product

GOAL = 100

def free_bacon(score):
    tens = score // 10
    ones = score % 10
    return 1 + max(tens, ones)

def roll_outcomes(n):
    if n == 0:
        return [None]
    return list(product([1, 2, 3, 4, 5, 6], repeat=n))

def score_from_roll(roll):
    if roll is None:
        return None
    if 1 in roll:
        return 1
    return sum(roll)


### EXPECTIMAX ###

def expectimax(score_me, score_opp, is_my_turn, depth):
    if score_me >= GOAL:
        return float('inf')
    if score_opp >= GOAL:
        return float('-inf')
    if depth == 0:
        return evaluation(score_me, score_opp)

    if is_my_turn:
        best_value = float('-inf')
        for n in range(0, 6):
            value = expectimax_action(score_me, score_opp, n, depth, opponent=False)
            best_value = max(best_value, value)
        return best_value
    else:
        # CHANCE node pentru adversar: presupun ca joaca mereu cu n = 4
        n = 4
        return expectimax_action(score_me, score_opp, n, depth, opponent=True)


def expectimax_action(score_me, score_opp, n, depth, opponent=False):
    outcomes = roll_outcomes(n)
    total = 0

    for outcome in outcomes:
        if outcome is None:
            gained = free_bacon(score_opp)
        else:
            gained = score_from_roll(outcome)

        if opponent:
            # muta adversarul
            new_me = score_me
            new_opp = score_opp + gained
            total += expectimax(new_me, new_opp, True, depth - 1)
        else:
            # mut eu
            new_me = score_me + gained
            new_opp = score_opp
            total += expectimax(new_me, new_opp, False, depth - 1)

    return total / len(outcomes)


def best_move(score_me, score_opp, depth=2):
    best_n = 0
    best_value = float('-inf')

    for n in range(0, 6):
        value = expectimax_action(score_me, score_opp, n, depth, opponent=False)
        if value > best_value:
            best_value = value
            best_n = n

    return best_n

print("TEST 1 PROBLEMA 2:")
print(best_move(50, 63, depth=2))

print("TEST 2 PROBLEMA 2:")
print(best_move(10, 99, depth=2))


print("TEST 3 PROBLEMA 2:")
print(best_move(95, 10, depth=2))
