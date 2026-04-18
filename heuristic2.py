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
def _(read_graph):
    graph = read_graph("gc_1000.txt")
    return (graph,)


@app.cell
def _(graph):
    graph
    return


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
                neighbor_colors = {
                    coloring[n] for n in self.graph[vertex] if n in coloring
                }
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

        def clamp_to_k_colors(
            self, coloring: Coloring, color_limit: int
        ) -> Coloring:
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

        def crossover_gpx(
            self, parent_a: Coloring, parent_b: Coloring, color_limit: int
        ) -> Coloring:
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
                    best_c = max(
                        classes_a.keys(),
                        key=lambda c: len(classes_a[c] & uncolored),
                        default=0,
                    )
                    chosen_set = classes_a[best_c] & uncolored
                else:
                    best_c = max(
                        classes_b.keys(),
                        key=lambda c: len(classes_b[c] & uncolored),
                        default=0,
                    )
                    chosen_set = classes_b[best_c] & uncolored

                for v in chosen_set:
                    child[v] = k

                uncolored -= chosen_set
                turn_a = not turn_a

            for v in uncolored:
                child[v] = self.rng.randrange(color_limit)

            return child

        def local_search(
                self, coloring: Coloring, color_limit: int, max_evals: int = 50
            ) -> None:
                conflict_nodes = [
                    u
                    for u in self.graph
                    if any(coloring[u] == coloring[v] for v in self.graph[u])
                ]

                if not conflict_nodes:
                    return

                self.rng.shuffle(conflict_nodes)
                evals = 0

                for u in conflict_nodes:
                    if evals >= max_evals:
                        break

                    current_color = coloring[u]
                    current_conflicts = sum(
                        1 for v in self.graph[u] if coloring[v] == current_color
                    )

                    best_color = current_color
                    min_conflicts = current_conflicts

                    colors = list(range(color_limit))
                    self.rng.shuffle(colors)

                    for c in colors:
                        if c == current_color:
                            continue

                        new_conflicts = sum(
                            1 for v in self.graph[u] if coloring[v] == c
                        )

                        if new_conflicts < min_conflicts:
                            min_conflicts = new_conflicts
                            best_color = c

                            if min_conflicts == 0:
                                break

                    if best_color != current_color:
                        coloring[u] = best_color

                    evals += 1
    
        # def local_search(
        #         self, coloring: Coloring, color_limit: int, max_evals: int = 50
        #     ) -> None:
            
        #         # Sweep to find nodes currently in conflict
        #         conflict_nodes = [
        #             u
        #             for u in self.graph
        #             if any(coloring[u] == coloring[v] for v in self.graph[u])
        #         ]

        #         if not conflict_nodes:
        #             return

        #         self.rng.shuffle(conflict_nodes)
        #         evals = 0
            
        #         # Pre-allocate the colors list ONCE
        #         base_colors = list(range(color_limit))

        #         for u in conflict_nodes:
        #             if evals >= max_evals:
        #                 break
                    

        #             current_color = coloring[u]
                
        #             # Fast counting (avoids generator overhead)
        #             current_conflicts = 0
        #             for v in self.graph[u]:
        #                 if coloring[v] == current_color:
        #                     current_conflicts += 1

        #             best_color = current_color
        #             min_conflicts = current_conflicts

        #             # Shuffle the pre-allocated list in-place
        #             self.rng.shuffle(base_colors)

        #             for c in base_colors:
        #                 if c == current_color:
        #                     continue

        #                 new_conflicts = 0
        #                 for v in self.graph[u]:
        #                     if coloring[v] == c:
        #                         new_conflicts += 1
        #                         # EARLY EXIT: If this color is already worse, stop checking
        #                         if new_conflicts >= min_conflicts:
        #                             break

        #                 # If we found a strictly better color, update our tracking
        #                 if new_conflicts < min_conflicts:
        #                     min_conflicts = new_conflicts
        #                     best_color = c

        #                     # If we found a perfect color, no need to check other colors
        #                     if min_conflicts == 0:
        #                         break

        #             if best_color != current_color:
        #                 coloring[u] = best_color

        #             evals += 1

        def mutate_coloring(
            self, coloring: Coloring, color_limit: int, mutation_probability: float
        ) -> None:
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
                self.mutate_coloring(
                    candidate, color_limit, mutation_probability=0.15
                )
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

                next_population = [
                    dict(ranked_population[index][0])
                    for index in range(elite_count)
                ]

                while len(next_population) < population_size:
                    parent_a = self.tournament_select(population, fitness_values)
                    parent_b = self.tournament_select(population, fitness_values)

                    child_a = self.crossover_gpx(parent_a, parent_b, color_limit)
                    child_b = self.crossover_gpx(parent_b, parent_a, color_limit)

                    self.mutate_coloring(
                        child_a, color_limit, mutation_probability
                    )
                    self.mutate_coloring(
                        child_b, color_limit, mutation_probability
                    )

                    if random.random() < 0.25:
                        self.local_search(child_a, color_limit, max_evals=20)
                    if random.random() < 0.25:
                        self.local_search(child_b, color_limit, max_evals=20)

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
                    print(
                        f"Failed to find coloring for k={color_limit}. Stopping."
                    )
                    break

                best_coloring = candidate
                best_color_limit = color_limit
                print(f"Success! Found feasible coloring with k={color_limit}")

            return best_coloring

    return (GraphColoringHeuristic,)


@app.cell
def _(GraphColoringHeuristic, graph):
    solver = GraphColoringHeuristic(graph, rng_seed=42)
    solution = solver.greedy_plus_ga(
        pop_size=30, generations=200, mutation_rate=0.04
    )
    print(f"Solution:\n{solution}")
    print(f"Chromatic number: {solver.num_colors(solution)}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
