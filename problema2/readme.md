# Problema 2.1 (Othello)

## 1. Explicație euristică

Euristica folosită combină trei lucruri:

- diferența dintre numărul de piese negre și albe
- diferența dintre numărul de mutări valide (mobilitate)
- diferența dintre numărul de colțuri ocupate

Formula este:

e(stare) = (black - white)
         + 5 * (mob_black - mob_white)
         + 25 * (corner_black - corner_white)

Justificare:

Numărul de piese arată avantajul brut.  
Mobilitatea arată cine controlează jocul, pentru că jucătorul cu mai multe mutări valide are mai multe opțiuni.  
Colțurile sunt foarte importante în Othello, pentru că nu pot fi întoarse, deci au pondere mare.

---

## 2. Minimax cu Alpha‑Beta (generalizat)

    def minimax(state, depth, alpha, beta, player):
        if depth == 0 or terminal(state):
            return evaluation(state), None
    
        if player == MAX:
            best_value = -inf
            best_move = None
    
            for move in generate_moves(state, player):
                new_state = apply_move(state, move, player)
                value, _ = minimax(new_state, depth-1, alpha, beta, MIN)
    
                if value > best_value:
                    best_value = value
                    best_move = move
    
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
    
            return best_value, best_move
    
        else:  # MIN
            best_value = +inf
            best_move = None
    
            for move in generate_moves(state, player):
                new_state = apply_move(state, move, player)
                value, _ = minimax(new_state, depth-1, alpha, beta, MAX)
    
                if value < best_value:
                    best_value = value
                    best_move = move
    
                beta = min(beta, value)
                if beta <= alpha:
                    break
    
            return best_value, best_move

---

# Problema 2.2 (Hog)

## 1. Explicație euristică

Euristica folosită este:

(score_me - score_opp)
+ 0.3 * free_bacon_potential
- 0.5 * danger

Unde:

free_bacon_potential = 1 + max(cifra zecilor adversarului, cifra unităților adversarului)  
danger = score_opp / 100

Justificare:

Diferența de scor este criteriul principal.  
Dacă adversarul are cifre mari, pot lua multe puncte cu n = 0, deci e un avantaj.  
Dacă adversarul este aproape de 100, este un pericol, deci scad scorul.

---

## 2. Expectimax (generalizat)

    def expectimax(state, depth, is_max_turn):
        if depth == 0 or terminal(state):
            return evaluation(state)
    
        if is_max_turn:
            best_value = -inf
    
            for action in actions(state):
                value = expectimax_chance(state, action, depth)
                best_value = max(best_value, value)
    
            return best_value
    
        else:
            return expectimax_chance(state, fixed_opponent_action, depth)

    def expectimax_chance(state, action, depth):
        outcomes = all_outcomes(action)
        total = 0
    
        for outcome in outcomes:
            new_state = apply_outcome(state, action, outcome)
            value = expectimax(new_state, depth-1, not is_opponent_turn)
            total += value
    
        return total / len(outcomes)

    def best_move(state, depth):
        best_action = None
        best_value = -inf
    
        for action in actions(state):
            value = expectimax_chance(state, action, depth)
            if value > best_value:
                best_value = value
                best_action = action
    
        return best_action


