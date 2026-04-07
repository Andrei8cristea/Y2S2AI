# 🧬 Proiect Algoritmi Genetici – Generare Labirint N×M

Acest proiect implementează un **algoritm genetic complet** pentru generarea unui labirint de dimensiune N×M, care conține:

- obiecte colectabile,
- pericole,
- zone blocate ce necesită chei,
- un sistem de energie,
- posibilitatea de a parcurge labirintul în mod interactiv.

Proiectul respectă integral cerințele temei.

---

# 1. Structura codului

Codul este organizat în module logice clare, fiecare responsabil pentru o parte a funcționalității.

---

## 1.1. CONSTANTE & CONFIG

### **Constante**
Definește codurile numerice pentru toate tipurile de celule:

- `WALL`, `PATH`, `START`, `EXIT`
- `KEY`, `LOCK`
- `FOOD`, `SHIELD`, `TREASURE`
- `MONSTER`, `POISON`, `TRAP`

### **load_config()**
Încarcă parametrii din `config.txt`:

- dimensiuni labirint (`N`, `M`)
- energie inițială
- procente pereți / pericole
- dimensiunea populației
- număr generații
- rata de mutație

---

## 1.2. GENERARE LABIRINT

### **generate_maze_dfs()**
Generează un labirint valid folosind **DFS randomizat**.

### **place_start_exit()**
Plasează START și EXIT în poziții fixe.

### **get_all_path_cells()**
Returnează toate celulele accesibile.

### **add_objects_and_dangers()**
Plasează obiecte colectabile și pericole:

- mâncare, scuturi, comori, chei
- monștri, otravă, capcane
- zone LOCK

### **generate_random_labyrinth()**
Generează un labirint complet folosind toate funcțiile de mai sus.

---

## 1.3. ANALIZA LABIRINTULUI

### **bfs_shortest_path()**
Calculează drumul optim dintre START și EXIT.

### **analyze_labyrinth()**
Calculează parametrii necesari pentru fitness:

- **ND** – număr de noduri de decizie (drumuri alternative)
- **LS** – lungimea soluției optime
- **NC** – număr de cotituri
- **NP** – număr total de pericole
- **NPI** – pereți complet izolați
- **PC** – procent pereți
- **explorare** – procent celule accesibile
- **path** – drumul optim

---

## 1.4. FITNESS

### **fitness()**
Evaluează complexitatea labirintului folosind:

- penalizare ND=0
- LS mare → scor mare
- NC mare → scor mare
- explorare mare → scor mare
- PC ∈ [20%, 40%]
- NP ∈ [5%, 15%]
- penalizare pereți izolați
- penalizare ND prea mare

---

## 1.5. ALGORITM GENETIC

### **generate_initial_population()**
Generează populația inițială.

### **evaluate_population()**
Calculează fitness-ul fiecărui labirint.

### **tournament_selection()**
Selectează părinți prin turneu.

### **crossover_quadrants()**
Combină cadrane din doi părinți.

### **mutate()**
Aplică mutații locale controlate.

### **run_ga()**
Rulează întregul algoritm genetic:

- selecție
- elitism
- crossover
- mutație
- evoluție pe generații

---

## 1.6. AFIȘARE LABIRINT

### **print_maze()**
Afișează labirintul + legenda în partea dreaptă.

---

## 1.7. GAMEPLAY

### **find_start()**
Găsește poziția START.

### **play_game()**
Permite utilizatorului să parcurgă labirintul:

- energie
- inventar
- efecte obiecte
- efecte pericole
- câștig / pierdere

---

## 1.8. MAIN

### **main**
- încarcă config
- rulează GA
- afișează cel mai bun labirint
- permite utilizatorului să îl joace

---

# 2. Explicarea cerințelor și modul în care sunt îndeplinite

---

## ✔ Cerința 1 (0.5p) – DFS randomizat

Implementată în:

- `generate_maze_dfs()`
- `generate_random_labyrinth()`
- `generate_initial_population()`

Populația inițială conține labirinturi valide.

---

## ✔ Cerința 2 (0.5p) – Obiecte, pericole, config din fișier

Obiecte colectabile:

- KEY, FOOD, SHIELD, TREASURE

Pericole:

- MONSTER, POISON, TRAP

Config încărcat din fișier:

- `load_config()`

---

## ✔ Cerința 3 (1p) – Funcție de fitness complexă

Parametri folosiți:

- ND – noduri de decizie
- LS – lungimea soluției
- NC – cotituri
- explorare – procent celule accesibile
- PC – procent pereți
- NP – pericole totale
- NPI – pereți izolați

Fitness-ul:

- penalizează ND=0
- penalizează ND prea mare
- favorizează LS mare
- favorizează NC mare
- favorizează explorare mare
- favorizează PC în [20%, 40%]
- favorizează NP în [5%, 15%]
- penalizează pereți izolați

Este complet diferită de exemplul din enunț și mult mai complexă.

---

## ✔ Cerința 4 (1p) – Algoritm genetic complet

Componente implementate:

- selecție: `tournament_selection`
- crossover: `crossover_quadrants`
- mutație: `mutate`
- elitism: top 10%
- cromozom = matrice labirint
- evoluție pe generații: `run_ga()`

---

# 3. Argumentarea alegerilor

---

### **DFS pentru generare inițială**
- produce labirinturi valide
- rapid și simplu
- garantat conectate

### **Tournament selection**
- stabil
- nu necesită normalizare
- evită dominarea unui singur individ

### **Crossover pe cadrane**
- păstrează structura globală
- reduce riscul de labirinturi imposibile

### **Mutație locală controlată**
- nu distruge conectivitatea
- introduce diversitate

### **Fitness multi-parametru**
- reflectă fidel complexitatea labirintului
- respectă toate cerințele profesorului
- penalizează labirinturile imposibile
- favorizează explorarea și dificultatea

### **Gameplay simplu**
- suficient pentru cerință
- demonstrează funcționalitatea obiectelor și pericolelor

---

