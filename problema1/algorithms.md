# 1. Explicatie Euristica

Euristica propusa: numarul de breakpoints din stiva

=> Practic trec prin stiva si oriunde am o nepotrivire(= breakpoint),adica dupa valoarea x nu urmeaza valoarea x-1 cresc numarul de breakpoints cu 1 sau altfel spus h(starea respectiva) += 1


Admisibilitate
=> un singur flip poate repara maxim un breakpoint deci rezulta ca nu poate supra estima sau altfel spus: h(stare) <= h*(stare)

Informativa
=> imi masoara exact dezordinea din stiva

---

# 2. A* Generalizat   


    import heapq
    
    def a_star(start):
        start_state = start
        goal_state = start_state  # processed
    
        pq = []
        heapq.heapify(pq)
        heapq.heappush(pq, (f, g, state, path))
    
        visited = set()
    
        while pq:
            f, g, state, path = heapq.heappop(pq)
    
            if state == goal_state:
                return path
    
            if state in visited:
                continue
    
            visited.add(state)
    
            for k in range(2, len(state) + 1):
                new_state = state  # processed
                new_g = g + cost
                new_h = heuristic(new_state)
                new_f = new_g + new_h
    
                heapq.heappush(pq, (new_f, new_g, new_state, path))
    
        return None

---

# IDA* Generalizat

    def ida_star(start):
        start_state = start
        goal_state = start_state  # processed
    
        def search(state, g, bound, path):
            f = g + heuristic(state)
            if f > bound:
                return f, None
            if state == goal_state:
                return True, path
    
            minimum = float('inf')
    
            for k in range(2, len(state) + 1):
                new_state = state  # processed
                new_g = g + cost
                t, sol = search(new_state, new_g, bound, path)
                if t is True:
                    return True, sol
                if t < minimum:
                    minimum = t
    
            return minimum, None
    
        bound = heuristic(start_state)
    
        while True:
            t, solution = search(start_state, 0, bound, [])
            if t is True:
                return solution
            bound = t

---
