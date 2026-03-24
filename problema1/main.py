# PROBLEMA 1
#######################################################


# 2


import heapq

#euristica cu breakpoints
def breakpoints(state):
    breakpoints_counter = 0
    for i in range(len(state)-1):
        if state[i] != state[i+1] + 1:
            breakpoints_counter += 1
    if state[-1] != 1:
        breakpoints_counter += 1
    return breakpoints_counter


def flip(state, k):
    return tuple(reversed(state[:k])) + state[k:]


def a_star(start_state):
    start_state = tuple(start_state)
    goal_state = tuple(x for x in range(1, len(start_state)+1,1))
    #goal_state = (1,2,3, ... n-1, n)

    pq = []
    heapq.heappush(pq, (breakpoints(start_state), 0, start_state, []))
    #pq = [(f(stare), g(stare), stare_propriu_zisa, path-ul pana la stare)]

    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if state == goal_state:
            return path

        if state in visited:
            continue

        visited.add(state)

        for k in range(2, len(state)+1):
            new_state = flip(state, k)
            new_g = g+1
            new_h = breakpoints(new_state)
            new_f = new_g + new_h
            heapq.heappush(pq, (new_f, new_g, new_state, path + [k]))

    return None

# 3

def ida_star(start_state):
    start_state = tuple(start_state)
    goal_state = tuple(x for x in range(1, len(start_state)+1,1))

    def search(state, g, bound, path):
        #depth search limitata de bound
        f = g + breakpoints(state)
        if f > bound:
            return f, None
        if state == goal_state:
            return True, path

        minimum = float('inf')

        for k in range(2, len(state)+1):
            new_state = flip(state, k)
            new_g = g+1
            t, sol = search(new_state, new_g, bound, path + [k])

            if t is True:
                return True, sol
            if t < minimum:
                minimum = t

        return minimum, None

    bound = breakpoints(start_state)

    while True:
        t, solution = search (start_state,0, bound, [])
        if t is True:
            return solution
        bound = t


#######################################################
# TESTARE

start = (4,3,2,1,5)
print(a_star(start))
print(ida_star(start))
