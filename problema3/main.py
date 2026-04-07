import random
import math
from collections import deque

######################### CONSTANTE #########################


WALL = 0
PATH = 1
START = 2
EXIT = 3
KEY = 4
LOCK = 5
FOOD = 6
SHIELD = 7
MONSTER = 8
POISON = 9
TREASURE = 10
TRAP = 11

def load_config(path="config.txt"):
    params = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                k, v = line.split("=")
                k = k.strip()
                v = v.strip()
                try:
                    if "." in v:
                        params[k] = float(v)
                    else:
                        params[k] = int(v)
                except ValueError:
                    params[k] = v
    except FileNotFoundError:
        #default if I can't open the file
        params = {
            "N": 21,
            "M": 21,
            "ENERGIE_INIT": 50,
            "MIN_PERC_PERETI": 0.2,
            "MAX_PERC_PERETI": 0.4,
            "MIN_PERC_PERICOLE": 0.05,
            "MAX_PERC_PERICOLE": 0.15,
            "POP_SIZE": 20,
            "GENERATIONS": 30,
            "MUTATION_RATE": 0.05
        }
    return params

#############  GENERARE LABIRIND -> DFS RANDOMIZAT #############

def generate_maze_dfs(n,m):
    maze = [[WALL for _ in range(m)] for _ in range (n)]
    visited = [[False for _ in range(m)] for _ in range(n)]

    def neighbors(i,j):
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(dirs)
        for di,dj in dirs:
            ni,nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
                yield ni,nj,di,dj

    start_i, start_j = 1,1
    maze[start_i][start_j] = PATH
    visited[start_i][start_j] = True
    stack = [(start_i,start_j)]

    while stack:
        i,j = stack[-1]
        found = False
        for ni,nj,di,dj in neighbors(i,j):
            visited[ni][nj] = True
            maze[ni][nj] = PATH
            maze[i+di//2][j+dj//2] = PATH
            stack.append((ni,nj))
            found = True
            break
        if not found:
            stack.pop()

    return maze


def place_start_exit(maze):
    n,m = len(maze), len(maze[0])
    maze[1][1] = START
    maze[n-2][m-2] = EXIT
    return (1,1), (n-2, m-2)


def get_all_path_cells(maze):
    cells = []

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in (PATH,START,EXIT):
                cells.append((i, j))

    return cells


def add_objects_and_dangers(maze, params):
    n,m = len(maze), len(maze[0])
    cells = get_all_path_cells(maze)
    random.shuffle(cells)

    total_cells = n*m
    min_perc_p = params.get("MIN_PERC_PERICOLE", 0.05)
    max_perc_p = params.get("MAX_PERC_PERICOLE", 0.15)

    target_perc_p = random.uniform(min_perc_p, max_perc_p)
    target_dangers = int(target_perc_p * total_cells)

    dangers_placed = 0
    for (i,j) in cells:
        if maze[i][j] in (START,EXIT):
            continue
        if dangers_placed < target_dangers and random.random() < 0.2:
            maze[i][j] = random.choice([MONSTER, POISON, TRAP])
            dangers_placed += 1
        else:
            if random.random() < 0.2:
                maze[i][j] = random.choice([FOOD, SHIELD, TREASURE, KEY])
    for (i,j) in cells[: len(cells)//10]:
        if maze[i][j] == PATH and random.random() < 0.2:
            maze[i][j] = LOCK

    return maze



def generate_random_labyrinth(params):
    n,m = params["N"], params["M"]
    maze = generate_maze_dfs(n,m)
    start,exit_ = place_start_exit(maze)
    maze = add_objects_and_dangers(maze, params)
    return maze

#################  ANALIZA LABIRINT  #################

def bfs_shortest_path(maze, start, exit_):
    n,m = len(maze), len(maze[0])
    si,sj = start
    ei, ej = exit_

    dirs = [ (-1,0), (1,0), (0,-1), (0,1) ]

    visited = [[False for _ in range(m)] for _ in range(n)]
    parent = [[None for _ in range(m)] for _ in range(n)]

    q = deque()
    q.append((si,sj))
    visited[si][sj] = True

    found = False

    while q:
        i,j = q.popleft()

        if (i,j) == (ei,ej):
            found = True
            break

        for di,dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m:
                if not visited[ni][nj] and maze[ni][nj] != WALL:
                    visited[ni][nj] = True
                    parent[ni][nj]= (i,j)
                    q.append((ni,nj))

    if not found:
        return None, [], visited

    path = []
    curr = (ei, ej)
    while curr:
        path.append(curr)
        curr = parent[curr[0]][curr[1]]

    path.reverse()

    return len(path), path, visited


def analyze_labyrinth(maze):
    n,m = len(maze), len(maze[0])

    start = None
    exit_ = None

    for i in range(n):
        for j in range(m):
            if maze[i][j] == START:
                start = (i,j)
            elif maze[i][j] == EXIT:
                exit_ = (i,j)

    dist, path, visited = bfs_shortest_path(maze, start, exit_)

    LS = dist if dist is not None else 0

    def count_turns(path):
        if len(path) < 3:
            return 0
        turns = 0
        for k in range(1, len(path) - 1):
            x1, y1 = path[k - 1]
            x2, y2 = path[k]
            x3, y3 = path[k + 1]
            dx1, dy1 = x2 - x1, y2 - y1
            dx2, dy2 = x3 - x2, y3 - y2
            if (dx1, dy1) != (dx2, dy2):
                turns += 1
        return turns

    NC = count_turns(path)

    NP = sum(maze[i][j] in (MONSTER, POISON, TRAP)
             for i in range(n) for j in range(m))

    def is_isolated_wall(i, j):
        if maze[i][j] != WALL:
            return False
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for di,dj in dirs:
            ni,nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < m:
                if maze[ni][nj] != WALL:
                    return False
        return True

    NPI = sum(is_isolated_wall(i,j) for i in range(n) for j in range(m))

    total_cells = n*m
    wall_count = sum(maze[i][j] == WALL for i in range(n) for j in range(m))
    PC = wall_count / total_cells if total_cells > 0 else 0

    accessible = sum(visited[i][j] for i in range(n) for j in range(m))
    explorare = accessible / (total_cells - wall_count) if (total_cells - wall_count) > 0 else 0

    ND = 0
    for i in range(n):
        for j in range(m):
            if maze[i][j] in (PATH, START, EXIT):
                deg = 0
                for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni,nj = i+di, j+dj
                    if 0 <= ni < n and 0 <= nj < m and maze[ni][nj] in (PATH,START,EXIT):
                        deg += 1
                if deg >= 3:
                    ND += 1

    return {
        "ND": ND,
        "LS": LS,
        "NC": NC,
        "NP": NP,
        "NPI": NPI,
        "PC": PC,
        "explorare": explorare,
        "path": path
    }


def fitness(stats):
    ND  = stats["ND"]
    LS  = stats["LS"]
    NC  = stats["NC"]
    NP  = stats["NP"]
    NPI = stats["NPI"]
    PC  = stats["PC"]
    explorare = stats["explorare"]

    if LS == 0:
        return -999999

    score = 0

    score += LS * 3
    score += NC * 2
    score += explorare * 50

    if ND == 0:
        score -= 50000
    else:
        score -= ND * 1.5

    if 0.2 <= PC <= 0.4:
        score += 200
    else:
        score -= abs(PC - 0.3) * 500

    if (NP / max(1, (1))) >= 0.05 and (NP / max(1, (1))) <= 0.15:
        score += NP * 5
    else:
        score -= abs((NP / max(1, (1))) - 0.1) * 300

    score -= NPI * 10

    return score


#######################   GA    #######################

def generate_initial_population(params):
    pop_size = params["POP_SIZE"]
    return [generate_random_labyrinth(params) for _ in range(pop_size)]


def evaluate_population(population):
    scored = []
    for maze in population:
        stats = analyze_labyrinth(maze)
        score = fitness(stats)
        scored.append((score, maze, stats))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def tournament_selection(scored, k=3):
    competitors = random.sample(scored, k)
    competitors.sort(key=lambda x: x[0], reverse=True)
    return competitors[0][1]


def crossover_quadrants(m1, m2):
    n, m = len(m1), len(m1[0])
    mid_i = n // 2
    mid_j = m // 2
    child = [[WALL for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if i < mid_i and j < mid_j:
                child[i][j] = m1[i][j]
            elif i < mid_i and j >= mid_j:
                child[i][j] = m2[i][j]
            elif i >= mid_i and j < mid_j:
                child[i][j] = m2[i][j]
            else:
                child[i][j] = m1[i][j]

    child[1][1] = START
    child[n - 2][m - 2] = EXIT
    return child


def mutate(maze, params):
    n, m = len(maze), len(maze[0])
    mutation_rate = params["MUTATION_RATE"]

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if random.random() < mutation_rate:
                if maze[i][j] in (START, EXIT):
                    continue
                if maze[i][j] == PATH:
                    maze[i][j] = random.choice(
                        [PATH, FOOD, SHIELD, TREASURE, MONSTER, POISON, TRAP, KEY, LOCK]
                    )
                elif maze[i][j] == WALL:
                    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if any(
                        0 <= i + di < n and 0 <= j + dj < m and maze[i + di][j + dj] != WALL
                        for di, dj in dirs
                    ):
                        maze[i][j] = PATH
                else:
                    if random.random() < 0.3:
                        maze[i][j] = PATH
    return maze


def run_ga(params):
    generations = params["GENERATIONS"]
    population = generate_initial_population(params)
    best_overall = None

    for gen in range(generations):
        scored = evaluate_population(population)
        best_in_gen = scored[0]
        if best_overall is None or best_in_gen[0] > best_overall[0]:
            best_overall = best_in_gen

        print(f"Generatia {gen}, best fitness = {best_in_gen[0]:.2f}")

        new_population = []
        elite_count = max(1, len(population) // 10)
        new_population.extend([maze for (_, maze, _) in scored[:elite_count]])

        while len(new_population) < len(population):
            p1 = tournament_selection(scored)
            p2 = tournament_selection(scored)
            child = crossover_quadrants(p1, p2)
            child = mutate(child, params)
            new_population.append(child)

        population = new_population

    best_score, best_maze, best_stats = best_overall
    return best_maze, best_stats


#####################################################################
def print_maze(maze, player_pos=None):
    n, m = len(maze), len(maze[0])
    symbols = {
        WALL: "███",
        PATH: "   ",
        START: " ◆ ",
        EXIT: " ◇ ",
        KEY: " | ",
        LOCK: " ■ ",
        FOOD: " ● ",
        SHIELD: " ◉ ",
        MONSTER: " ☠ ",
        POISON: " ▲ ",
        TREASURE: " ♦ ",
        TRAP: " ▲ "
    }

    legend = [
        "LEGEND:",
        "◆ = START",
        "◇ = EXIT",
        "| = KEY",
        "■ = LOCK",
        "● = FOOD",
        "◉ = SHIELD",
        "☠ = MONSTER",
        "▲ = POISON/TRAP",
        "♦ = TREASURE"
    ]

    max_row_len = m * 3

    for i in range(n):
        row = ""
        for j in range(m):
            if player_pos and (i, j) == player_pos:
                row += " @ "
            else:
                row += symbols.get(maze[i][j], "?")

        row = row.ljust(max_row_len)

        if i < len(legend):
            print(row + "   " + legend[i])
        else:
            print(row)

################    GAMEPLAY    ################

def find_start(maze):
    n, m = len(maze), len(maze[0])
    for i in range(n):
        for j in range(m):
            if maze[i][j] == START:
                return (i, j)
    return None

def play_game(maze, params):
    n, m = len(maze), len(maze[0])
    player_pos = find_start(maze)
    if player_pos is None:
        print("Nu exista START in labirint.")
        return

    energie = params["ENERGIE_INIT"]
    step_cost = 1

    inventory = {
        "keys": 0,
        "shields": 0,
        "treasure": 0
    }

    dirs = {
        'w': (-1, 0),
        's': (1, 0),
        'a': (0, -1),
        'd': (0, 1)
    }

    while True:
        print_maze(maze, player_pos)
        print(f"Energie: {energie} (cost pas: {step_cost})")
        print(f"Inventar: {inventory}")
        move = input("Mutare (w/a/s/d, q pentru iesire): ").strip().lower()

        if move == 'q':
            print("Ai iesit din joc.")
            break

        if move not in dirs:
            print("Comanda invalida.")
            continue

        di, dj = dirs[move]
        pi, pj = player_pos
        ni, nj = pi + di, pj + dj

        if not (0 <= ni < n and 0 <= nj < m):
            print("Nu poti iesi din labirint.")
            continue

        cell = maze[ni][nj]

        if cell == WALL:
            print("Perete.")
            continue

        if cell == LOCK:
            if inventory["keys"] > 0:
                inventory["keys"] -= 1
                print("Ai folosit o cheie pentru a deschide zona blocata.")
                maze[ni][nj] = PATH
            else:
                print("Ai nevoie de o cheie pentru a trece.")
                continue

        energie -= step_cost
        if energie <= 0:
            print("Ai ramas fara energie. Game over.")
            break

        player_pos = (ni, nj)
        cell = maze[ni][nj]

        if cell == FOOD:
            energie += 10
            print("Ai mancat. Energie +10.")
            maze[ni][nj] = PATH

        elif cell == SHIELD:
            inventory["shields"] += 1
            print("Ai luat un scut.")
            maze[ni][nj] = PATH

        elif cell == TREASURE:
            inventory["treasure"] += 1
            print("Ai gasit o comoara.")
            maze[ni][nj] = PATH

        elif cell == KEY:
            inventory["keys"] += 1
            print("Ai gasit o cheie.")
            maze[ni][nj] = PATH

        elif cell == MONSTER:
            if inventory["shields"] > 0:
                inventory["shields"] -= 1
                print("Scutul te-a protejat de monstru.")
            else:
                energie -= 10
                print("Te-ai luptat cu un monstru. Energie -10.")
            maze[ni][nj] = PATH

        elif cell == POISON:
            energie += 5
            step_cost = 2
            print("Ai mancat mancare otravita. Energie +5, cost pas +1.")
            maze[ni][nj] = PATH

        elif cell == TRAP:
            energie -= 15
            print("Ai calcat intr-o capcana. Energie -15.")
            maze[ni][nj] = PATH

        elif cell == EXIT:
            print(f"Ai ajuns la iesire! Ai castigat. Ai colectat {inventory["treasure"]} comori!!!")
            break

        if energie <= 0:
            print("Ai ramas fara energie. Game over.")
            break


################      MAIN      ################

if __name__ == "__main__":
    params = load_config()
    best_maze, best_stats = run_ga(params)
    print("Labirintul cel mai bun gasit:")
    print_maze(best_maze)
    print("Statistici:", best_stats)

    ans = input("Vrei sa joci acest labirint? (y/n): ").strip().lower()
    if ans == 'y':
        play_game(best_maze, params)
# params = load_config()
# best_maze, best_stats = run_ga(params)
# print_maze(best_maze,(3,3))