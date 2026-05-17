# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo"]
# ///

import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    from greedy_algorithm import read_graph

    return (read_graph,)


@app.cell
def _():
    import random

    return (random,)


@app.cell
def _():
    from ga import wczytaj_dowolny_graf, greedy, ga_kolorowanie

    return ga_kolorowanie, greedy, wczytaj_dowolny_graf


@app.cell
def _(read_graph):
    graph = read_graph("gc1000.txt")
    return (graph,)


@app.cell
def _():
    import time

    return (time,)


@app.cell
def _(Coloring, Graph, List, Optional, random):
    class GraphColoringHeuristic:
        def __init__(self, graph: Graph, rng_seed: int = 42) -> None:
            self.graph = graph
            self.rng = random.Random(rng_seed)

        def greedy_coloring(self) -> Coloring:
            coloring: Coloring = {}
            for vertex in sorted(self.graph):
                color = 0
                neighbor_colors = {coloring[n] for n in self.graph[vertex] if n in coloring}
                while color in neighbor_colors:
                    color += 1
                coloring[vertex] = color
            return coloring

        def conflict_count(self, coloring: Coloring) -> int:
            conflicts = 0
            for u in self.graph:
                cu = coloring[u]
                for v in self.graph[u]:
                    if u < v and cu == coloring[v]:
                        conflicts += 1
            return conflicts

        def num_colors(self, coloring: Coloring) -> int:
            return len(set(coloring.values()))

        def clamp_to_k_colors(self, coloring: Coloring, color_limit: int) -> Coloring:
            clamped_coloring: Coloring = {}
            for vertex, color in coloring.items():
                if color < color_limit:
                    clamped_coloring[vertex] = color
                else:
                    clamped_coloring[vertex] = self.rng.randrange(color_limit)
            return clamped_coloring

        def tournament_select(
            self,
            population: List[Coloring],
            fitness_values: List[float],
            tournament_size: int = 3,
        ) -> Coloring:
            best_idx = -1
            best_fitness = -1.0

            for _ in range(tournament_size):
                idx = self.rng.randrange(len(population))
                if fitness_values[idx] > best_fitness:
                    best_fitness = fitness_values[idx]
                    best_idx = idx

            return population[best_idx]

        def crossover_gpx(self, parent_a: Coloring, parent_b: Coloring, color_limit: int) -> Coloring:
            child: Coloring = {}
            uncolored = set(parent_a.keys())

            classes_a = {c: set() for c in range(color_limit)}
            classes_b = {c: set() for c in range(color_limit)}

            for v, c in parent_a.items():
                classes_a[c].add(v)
            for v, c in parent_b.items():
                classes_b[c].add(v)

            turn_a = True
            for k in range(color_limit):
                if turn_a:
                    best_c = max(classes_a.keys(), key=lambda c: len(classes_a[c] & uncolored), default=0)
                    chosen_set = classes_a[best_c] & uncolored
                else:
                    best_c = max(classes_b.keys(), key=lambda c: len(classes_b[c] & uncolored), default=0)
                    chosen_set = classes_b[best_c] & uncolored

                for v in chosen_set:
                    child[v] = k

                uncolored -= chosen_set
                turn_a = not turn_a

            for v in uncolored:
                child[v] = self.rng.randrange(color_limit)

            return child

        def local_search(self, coloring: Coloring, color_limit: int, max_steps: int = 50) -> None:
            vertices = list(self.graph.keys())

            for _ in range(max_steps):
                improved = False
                self.rng.shuffle(vertices)

                for u in vertices:
                    current_color = coloring[u]
                    current_conflicts = sum(1 for v in self.graph[u] if coloring[v] == current_color)

                    if current_conflicts == 0:
                        continue

                    best_color = current_color
                    min_conflicts = current_conflicts

                    colors = list(range(color_limit))
                    self.rng.shuffle(colors)

                    for c in colors:
                        if c == current_color:
                            continue
                        new_conflicts = sum(1 for v in self.graph[u] if coloring[v] == c)
                        if new_conflicts < min_conflicts:
                            min_conflicts = new_conflicts
                            best_color = c

                    if best_color != current_color:
                        coloring[u] = best_color
                        improved = True

                if not improved:
                    break

        def mutate_coloring(self, coloring: Coloring, color_limit: int, mutation_probability: float) -> None:
            for vertex in list(coloring.keys()):
                if self.rng.random() < mutation_probability:
                    coloring[vertex] = self.rng.randrange(color_limit)

        def ga_find_feasible_k(
            self,
            initial_coloring: Coloring,
            color_limit: int,
            population_size: int = 60,
            generation_count: int = 300,
            mutation_probability: float = 0.03,
            elite_count: int = 2,
        ) -> Optional[Coloring]:
            population: List[Coloring] = []
            seeded_coloring = self.clamp_to_k_colors(initial_coloring, color_limit)
            self.local_search(seeded_coloring, color_limit)
            population.append(seeded_coloring)

            for _ in range(population_size - 1):
                candidate = dict(seeded_coloring)
                self.mutate_coloring(candidate, color_limit, mutation_probability=0.15)
                self.local_search(candidate, color_limit)
                population.append(candidate)

            for _ in range(generation_count):
                fitness_values = [
                    1.0 / (1.0 + self.conflict_count(candidate))
                    for candidate in population
                ]

                best_candidate_index = max(
                    range(len(population)),
                    key=lambda index: fitness_values[index],
                )

                if fitness_values[best_candidate_index] == 1.0:
                    return population[best_candidate_index]

                ranked_population = sorted(
                    zip(population, fitness_values),
                    key=lambda pair: pair[1],
                    reverse=True,
                )

                next_population = [dict(ranked_population[index][0]) for index in range(elite_count)]

                while len(next_population) < population_size:
                    parent_a = self.tournament_select(population, fitness_values)
                    parent_b = self.tournament_select(population, fitness_values)

                    child_a = self.crossover_gpx(parent_a, parent_b, color_limit)
                    child_b = self.crossover_gpx(parent_b, parent_a, color_limit)

                    self.mutate_coloring(child_a, color_limit, mutation_probability)
                    self.mutate_coloring(child_b, color_limit, mutation_probability)

                    self.local_search(child_a, color_limit, max_steps=10)
                    self.local_search(child_b, color_limit, max_steps=10)

                    next_population.append(child_a)
                    if len(next_population) < population_size:
                        next_population.append(child_b)

                population = next_population

            return None

        def greedy_plus_ga(
            self,
            pop_size: int = 60,
            generations: int = 300,
            mutation_rate: float = 0.03,
        ) -> Coloring:
            best_coloring = self.greedy_coloring()
            best_color_limit = self.num_colors(best_coloring)

            print(f"Initial Greedy coloring used k={best_color_limit}")

            for color_limit in range(best_color_limit - 1, 0, -1):
                print(f"Searching for feasible coloring with k={color_limit}...")
                candidate = self.ga_find_feasible_k(
                    initial_coloring=best_coloring,
                    color_limit=color_limit,
                    population_size=pop_size,
                    generation_count=generations,
                    mutation_probability=mutation_rate,
                    elite_count=2,
                )
                if candidate is None:
                    print(f"Failed to find coloring for k={color_limit}. Stopping.")
                    break

                best_coloring = candidate
                best_color_limit = color_limit
                print(f"Success! Found feasible coloring with k={color_limit}")

            return best_coloring

    return (GraphColoringHeuristic,)


@app.cell
def _(GraphColoringHeuristic, graph):
    solver = GraphColoringHeuristic(graph, rng_seed=32)
    solution = solver.greedy_plus_ga(pop_size=20, generations=100, mutation_rate=0.04)
    print(f"Solution:\n{solution}")
    print(f"Chromatic number: {solver.num_colors(solution)}")
    return


@app.cell
def _(random):
    from collections import Counter
    from typing import Dict, Set, Tuple

    def greedy_init(graph: Dict[int, Set[int]]) -> Dict[int, int]:
        coloring: Dict[int, int] = {}
        for v in sorted(graph):
            used = {coloring[n] for n in graph[v] if n in coloring}
            c = 1
            while c in used:
                c += 1
            coloring[v] = c
        return coloring

    def conflict_count(graph: Dict[int, Set[int]], coloring: Dict[int, int]) -> int:
        seen = set()
        conflicts = 0
        for u, neigh in graph.items():
            for v in neigh:
                if (v, u) in seen:
                    continue
                seen.add((u, v))
                if coloring.get(u) == coloring.get(v):
                    conflicts += 1
        return conflicts

    def tabu_search(
        graph: Dict[int, Set[int]],
        max_iters: int = 1000,
        tabu_tenure: int = 7,
        init_method: str = "greedy",
        seed: int | None = None,
    ) -> Dict[int, int]:
        if seed is not None:
            random.seed(seed)

        # init
        if init_method == "random":
            current = {v: random.randint(1, max(1, len(graph))) for v in graph}
        else:
            current = greedy_init(graph)

        best = dict(current)
        current_conflicts = conflict_count(graph, current)
        best_conflicts = current_conflicts
        best_colors = len(set(best.values()))
        tabu: Dict[Tuple[int, int], int] = {}

        for it in range(1, max_iters + 1):
            max_color = max(current.values())
            # build candidate moves: (vertex, target_color)
            best_move = None
            best_move_key = None

            for v in graph:
                old_color = current[v]
                old_conflicts_v = sum(1 for n in graph[v] if current.get(n) == old_color)
                for new_color in range(1, max_color + 1):
                    if new_color == old_color:
                        continue
                    new_conflicts_v = sum(1 for n in graph[v] if current.get(n) == new_color)
                    delta = new_conflicts_v - old_conflicts_v
                    new_total_conflicts = current_conflicts + delta

                    occurrences_old = sum(1 for col in current.values() if col == old_color)
                    would_reduce = occurrences_old == 1 and new_color != old_color
                    candidate_key = (v, new_color)
                    is_tabu = tabu.get(candidate_key, 0) > it

                    # aspiration: allow tabu if it improves best known (colors first, then conflicts)
                    candidate_colors = len(set((current[v] if k != v else new_color) for k in current))
                    aspiration = False
                    if is_tabu:
                        if candidate_colors < best_colors:
                            aspiration = True
                        elif candidate_colors == best_colors and new_total_conflicts < best_conflicts:
                            aspiration = True

                    if is_tabu and not aspiration:
                        continue

                    # objective: prefer moves that reduce color count, then reduce conflicts
                    key = (0 if would_reduce else 1, new_total_conflicts, random.random())
                    if best_move is None or key < best_move_key:
                        best_move = (v, new_color, old_color, delta, would_reduce)
                        best_move_key = key

            if best_move is None:
                break  # no move available

            v, new_color, old_color, delta, would_reduce = best_move
            # apply move
            current[v] = new_color
            current_conflicts += delta
            tabu[(v, old_color)] = it + tabu_tenure

            # update best
            current_colors = len(set(current.values()))
            if current_colors < best_colors or (current_colors == best_colors and current_conflicts < best_conflicts):
                best = dict(current)
                best_colors = current_colors
                best_conflicts = current_conflicts

            # quick exit if perfect 1-color (rare)
            if best_conflicts == 0 and best_colors == 1:
                break

        return best

    return conflict_count, tabu_search


@app.cell
def _(conflict_count, graph, read_graph, tabu_search):
    graph2 = read_graph("gc500.txt", undirected=True)
    best_col = tabu_search(graph2, max_iters=200, tabu_tenure=10, init_method="greedy", seed=42)
    print("colors:", len(set(best_col.values())), "conflicts:", conflict_count(graph, best_col))
    return


@app.cell
def _(ga_kolorowanie, greedy, time, wczytaj_dowolny_graf):
    instancje = [
        "queen6.txt",
        "miles250.txt",
        "gc500.txt",
        "gc1000.txt",
        "le450_5a.txt"
    ]

    GA_DLUGOSC = 30
    LIMIT_CZASOWY = 180

    print(f"Instancja GA Czas (s)")

    for plik in instancje:
        graf = wczytaj_dowolny_graf(plik)

        wynik_zachlanny = greedy(graf)
        kolory_startowe = max(wynik_zachlanny.values())

        start_ga = time.perf_counter()
        wynik_koncowy = ga_kolorowanie(
            graf,
            wynik_zachlanny,
            max_iter=7500,
            ga_dlugosc=GA_DLUGOSC,
            max_czas=LIMIT_CZASOWY
        )
        czas_wykonania = time.perf_counter() - start_ga
        kolory_koncowe = max(wynik_koncowy.values())

        print(f"{plik} {kolory_koncowe} {czas_wykonania}")
    return


if __name__ == "__main__":
    app.run()
