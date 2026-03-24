import heapq
from collections import deque
import copy

class Nod:
    def __init__(self,informatie,parinte = None):
        self.informatie = informatie
        self.parinte = parinte
        self.succesori = []
    def drumRadacina(self):
        nod_curent = self
        drum = []
        while nod_curent is not None:
            drum.insert(0, nod_curent)
            nod_curent = nod_curent.parinte
        return drum

    def vizitat(self):
        nod_curent = self.parinte
        while nod_curent is not None:
            if nod_curent.informatie == self.informatie:
                return True
            nod_curent = nod_curent.parinte
        return False

    def __str__(self):
        drum = self.drumRadacina()
        sageti_drum = "->".join([str(n.informatie) for n in drum])
        return f"{self.informatie} ({sageti_drum})"
    def __repr__(self):
        return str(self.informatie)


class Graf:
    def __init__(self, nodStart, noduriScop):
        self.nodStart = nodStart
        self.noduriScop = noduriScop

    def scop(self, informatie_nod):
        return informatie_nod == self.noduriScop

    def succesori(self, nod):
        succ = []
        stive_crt = nod.informatie
        for i in range(len(stive_crt)):
            if not stive_crt[i]:
                continue
            stive_copy = copy.deepcopy(stive_crt)
            bloc = stive_copy[i].pop()
            for j in range(len(stive_crt)):
                if i == j:
                    continue
                conf = copy.deepcopy(stive_copy)
                conf[j].append(bloc)

                nod_nou = Nod(informatie=conf,parinte = nod)

                if not nod_nou.vizitat():
                    succ.append(nod_nou)

        return succ
def consistenta(info_nod_crt,info_scop):
    h = 0;
    for i in range(len(info_nod_crt)):
        stiva_crt = info_nod_crt[i]
        stiva_scop = info_scop[i]

        for j in range(len(stiva_crt)):
            if j >= len(stiva_scop) or stiva_crt[j] != stiva_scop[j]:
                h+=1
    return h


def neconsistenta(info_nod, info_scop):
    if info_nod == info_scop:
        return 0

    h_baza = consistenta(info_nod, info_scop)

    if len(info_nod[0]) % 2 == 1:
        return 0.1
    return min(1, h_baza)

def neadmisibila(info_nod, info_scop):
    h = 0
    for i in range(len(info_nod)):
        stiva_crt = info_nod[i]
        stiva_scop = info_scop[i]
        for j in range(len(stiva_crt)):
            if j >= len(stiva_scop) or stiva_crt[j] != stiva_scop[j]:
                h += 67
    return h

def bfs(graf):
    start_info = copy.deepcopy(graf.nodStart)
    nod_start = Nod(informatie=start_info)

    if graf.scop(nod_start.informatie):
        return [nod_start]

    coada = deque([nod_start])

    while coada:
        nod_curent = coada.popleft()

        for succesor in graf.succesori(nod_curent):
            if graf.scop(succesor.informatie):
                return succesor.drumRadacina()
            coada.append(succesor)

    return None

def afisare(drum):
    if not drum:
        print("No drum")
        return
    for i, nod in enumerate(drum):
        print(f"{i}. {nod.informatie}")


def a_star(graf, scop):
    start_info = copy.deepcopy(graf.nodStart)
    nod_start = Nod(informatie=start_info)

    # g(n) pentru primul nod
    g_cost = {str(nod_start.informatie): 0}

    #priority queue
    pq = []
    heapq.heappush(pq, (scop(nod_start.informatie)))


start = [['B','A'],[],['D','C']]

scop = [['A'],['C','B'],['D']]

prob = Graf(start,scop)
rez = bfs(prob)
afisare(rez)
