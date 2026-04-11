import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from greedy_algorithm import read_graph

    return (read_graph,)


@app.cell
def _(read_graph):
    graph = read_graph("instance.txt")
    return (graph,)


@app.cell
def _():
    """import random

    def greedy_coloring(graph):
        coloring = {}

        for vertex in graph:
            color = 0

            neighbor_colors = {coloring[n] for n in graph[vertex] if n in coloring}
            while color in neighbor_colors:
                color += 1

            coloring[vertex] = color
        return coloring


    def conflict_count(graph: Graph, coloring: Coloring) -> int:
        conflicts = 0
        for u in graph:
            cu = coloring[u]
            for v in graph[u]:
                if u < v and cu == coloring[v]:
                    conflicts += 1
        return conflicts


    def num_colors(coloring: Coloring) -> int:
        return len(set(coloring.values()))


    def fitness_for_k(graph: Graph, coloring: Coloring) -> float:
        # For fixed k, minimize conflicts.
        # 1.0 means perfect (zero conflicts).
        c = conflict_count(graph, coloring)
        return 1.0 / (1.0 + c)

    def clamp_to_k_colors(coloring: Coloring, color_limit: int) -> Coloring:
        "Force every color into the range [0, color_limit - 1]."
        clamped_coloring: Coloring = {}
        for vertex, color in coloring.items():
            if color < color_limit:
                clamped_coloring[vertex] = color
            else:
                clamped_coloring[vertex] = random.randrange(color_limit)
        return clamped_coloring


    def roulette_select(
        candidate_colorings: List[Coloring],
        fitness_values: List[float],
    ) -> Coloring:
        fitness_sum = sum(fitness_values)
        if fitness_sum <= 0:
            return random.choice(candidate_colorings)

        selection_threshold = random.random() * fitness_sum
        cumulative_fitness = 0.0

        for candidate_coloring, fitness in zip(candidate_colorings, fitness_values):
            cumulative_fitness += fitness
            if cumulative_fitness >= selection_threshold:
                return candidate_coloring

        return candidate_colorings[-1]


    def crossover_uniform(
        parent_coloring_a: Coloring,
        parent_coloring_b: Coloring,
    ) -> Tuple[Coloring, Coloring]:
        child_coloring_a: Coloring = {}
        child_coloring_b: Coloring = {}

        for vertex in parent_coloring_a.keys():
            if random.random() < 0.5:
                child_coloring_a[vertex] = parent_coloring_a[vertex]
                child_coloring_b[vertex] = parent_coloring_b[vertex]
            else:
                child_coloring_a[vertex] = parent_coloring_b[vertex]
                child_coloring_b[vertex] = parent_coloring_a[vertex]

        return child_coloring_a, child_coloring_b


    def mutate_coloring(
        graph: Graph,
        coloring: Coloring,
        color_limit: int,
        mutation_probability: float,
    ) -> None:
        vertices = list(coloring.keys())

        for vertex in vertices:
            if random.random() < mutation_probability:
                coloring[vertex] = random.randrange(color_limit)

        for vertex in vertices:
            if any(coloring[vertex] == coloring[neighbor] for neighbor in graph[vertex]):
                if random.random() < 0.5:
                    coloring[vertex] = random.randrange(color_limit)


    def ga_find_feasible_k(
        graph: Graph,
        initial_coloring: Coloring,
        color_limit: int,
        population_size: int = 60,
        generation_count: int = 300,
        mutation_probability: float = 0.03,
        elite_count: int = 2,
    ) -> Optional[Coloring]:
        population: List[Coloring] = []
        seeded_coloring = clamp_to_k_colors(initial_coloring, color_limit)
        population.append(seeded_coloring)

        for _ in range(population_size - 1):
            candidate = dict(seeded_coloring)
            mutate_coloring(graph, candidate, color_limit, mutation_probability=0.15)
            population.append(candidate)

        for _generation in range(generation_count):
            fitness_values = [
                1.0 / (1.0 + conflict_count(graph, candidate))
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
                parent_a = roulette_select(population, fitness_values)
                parent_b = roulette_select(population, fitness_values)

                child_a, child_b = crossover_uniform(parent_a, parent_b)
                mutate_coloring(graph, child_a, color_limit, mutation_probability)
                mutate_coloring(graph, child_b, color_limit, mutation_probability)

                next_population.append(child_a)
                if len(next_population) < population_size:
                    next_population.append(child_b)

            population = next_population

        return None


    def greedy_plus_ga(
        graph: Graph,
        pop_size: int = 60,
        generations: int = 300,
        mutation_rate: float = 0.03,
        rng_seed: int = 42,
    ) -> Coloring:
        random.seed(rng_seed)

        best_coloring = greedy_coloring(graph)
        best_color_limit = num_colors(best_coloring)

        for color_limit in range(best_color_limit - 1, 0, -1):
            candidate = ga_find_feasible_k(
                graph=graph,
                initial_coloring=best_coloring,
                color_limit=color_limit,
                population_size=pop_size,
                generation_count=generations,
                mutation_probability=mutation_rate,
                elite_count=2,
            )
            if candidate is None:
                break

            best_coloring = candidate
            best_color_limit = color_limit
            print(f"Found feasible coloring with k={color_limit}")

        return best_coloring


    if __name__ == "__main__":
        #graph = read_graph("instance.txt")
        solution = greedy_plus_ga(
            graph,
            pop_size=80,
            generations=400,
            mutation_rate=0.04,
            rng_seed=123,
        )

        print("Final conflicts:", conflict_count(graph, solution))
        print("Final colors used:", num_colors(solution))"""
    return


@app.cell
def _():
    import random
    from typing import List, Tuple, Dict, Optional, Set

    # Type aliases for clarity
    Graph = Dict[int, List[int]]
    Coloring = Dict[int, int]

    def greedy_coloring(graph: Graph) -> Coloring:
        coloring: Coloring = {}
        for vertex in graph:
            color = 0
            neighbor_colors = {coloring[n] for n in graph[vertex] if n in coloring}
            while color in neighbor_colors:
                color += 1
            coloring[vertex] = color
        return coloring


    def conflict_count(graph: Graph, coloring: Coloring) -> int:
        conflicts = 0
        for u in graph:
            cu = coloring[u]
            for v in graph[u]:
                if u < v and cu == coloring[v]:
                    conflicts += 1
        return conflicts


    def num_colors(coloring: Coloring) -> int:
        return len(set(coloring.values()))


    def clamp_to_k_colors(coloring: Coloring, color_limit: int) -> Coloring:
        """Force every color into the range [0, color_limit - 1]."""
        clamped_coloring: Coloring = {}
        for vertex, color in coloring.items():
            if color < color_limit:
                clamped_coloring[vertex] = color
            else:
                clamped_coloring[vertex] = random.randrange(color_limit)
        return clamped_coloring


    def tournament_select(
        population: List[Coloring], 
        fitness_values: List[float], 
        tournament_size: int = 3
    ) -> Coloring:
        """
        Tournament selection is less prone to premature convergence 
        than Roulette Wheel selection.
        """
        best_idx = -1
        best_fitness = -1.0

        for _ in range(tournament_size):
            idx = random.randrange(len(population))
            if fitness_values[idx] > best_fitness:
                best_fitness = fitness_values[idx]
                best_idx = idx

        return population[best_idx]


    def crossover_gpx(parent_a: Coloring, parent_b: Coloring, color_limit: int) -> Coloring:
        """
        Greedy Partition Crossover (GPX).
        Breeds independent sets (color classes) rather than raw integers,
        solving the permutation/symmetry problem.
        """
        child: Coloring = {}
        uncolored = set(parent_a.keys())

        # Group vertices by color for both parents
        classes_a = {c: set() for c in range(color_limit)}
        classes_b = {c: set() for c in range(color_limit)}
        for v, c in parent_a.items(): classes_a[c].add(v)
        for v, c in parent_b.items(): classes_b[c].add(v)

        turn_a = True
        for k in range(color_limit):
            if turn_a:
                # Find largest color class in A (only considering uncolored vertices)
                best_c = max(classes_a.keys(), key=lambda c: len(classes_a[c] & uncolored), default=0)
                chosen_set = classes_a[best_c] & uncolored
            else:
                # Find largest color class in B
                best_c = max(classes_b.keys(), key=lambda c: len(classes_b[c] & uncolored), default=0)
                chosen_set = classes_b[best_c] & uncolored

            # Assign color k to the chosen set in the child
            for v in chosen_set:
                child[v] = k

            uncolored -= chosen_set
            turn_a = not turn_a

        # Any remaining uncolored vertices get a random color
        for v in uncolored:
            child[v] = random.randrange(color_limit)

        return child


    def local_search(graph: Graph, coloring: Coloring, color_limit: int, max_steps: int = 50) -> None:
        """
        A 1-opt Hill Climber using Delta Evaluation.
        Instead of checking the whole graph, it only counts conflicts for the moving vertex.
        """
        vertices = list(graph.keys())

        for _ in range(max_steps):
            improved = False
            random.shuffle(vertices)

            for u in vertices:
                current_color = coloring[u]

                # Count current conflicts for vertex u only
                current_conflicts = sum(1 for v in graph[u] if coloring[v] == current_color)

                if current_conflicts == 0:
                    continue  # Vertex is safe, don't move it

                best_color = current_color
                min_conflicts = current_conflicts

                # Try all other colors to find the one that minimizes conflicts
                colors = list(range(color_limit))
                random.shuffle(colors) # Prevent deterministic looping

                for c in colors:
                    if c == current_color:
                        continue
                    # Delta evaluation: only check neighbors
                    new_conflicts = sum(1 for v in graph[u] if coloring[v] == c)
                    if new_conflicts < min_conflicts:
                        min_conflicts = new_conflicts
                        best_color = c

                if best_color != current_color:
                    coloring[u] = best_color
                    improved = True

            # If we went through all vertices and couldn't improve, we hit a local optimum
            if not improved:
                break


    def mutate_coloring(coloring: Coloring, color_limit: int, mutation_probability: float) -> None:
        """Simple random mutation. The heavy lifting is now done by Local Search."""
        for vertex in list(coloring.keys()):
            if random.random() < mutation_probability:
                coloring[vertex] = random.randrange(color_limit)


    def ga_find_feasible_k(
        graph: Graph,
        initial_coloring: Coloring,
        color_limit: int,
        population_size: int = 60,
        generation_count: int = 300,
        mutation_probability: float = 0.03,
        elite_count: int = 2,
    ) -> Optional[Coloring]:

        population: List[Coloring] = []
        seeded_coloring = clamp_to_k_colors(initial_coloring, color_limit)
        local_search(graph, seeded_coloring, color_limit) # Optimize the seed
        population.append(seeded_coloring)

        # Initialize rest of population
        for _ in range(population_size - 1):
            candidate = dict(seeded_coloring)
            mutate_coloring(candidate, color_limit, mutation_probability=0.15)
            local_search(graph, candidate, color_limit)
            population.append(candidate)

        for _generation in range(generation_count):
            fitness_values = [
                1.0 / (1.0 + conflict_count(graph, candidate))
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
                parent_a = tournament_select(population, fitness_values)
                parent_b = tournament_select(population, fitness_values)

                # GPX breeds 1 child. We swap parent order to generate a 2nd distinct child
                child_a = crossover_gpx(parent_a, parent_b, color_limit)
                child_b = crossover_gpx(parent_b, parent_a, color_limit) 

                mutate_coloring(child_a, color_limit, mutation_probability)
                mutate_coloring(child_b, color_limit, mutation_probability)

                # MEMETIC UPGRADE: Local search applied to children before adding to population
                local_search(graph, child_a, color_limit, max_steps=10)
                local_search(graph, child_b, color_limit, max_steps=10)

                next_population.append(child_a)
                if len(next_population) < population_size:
                    next_population.append(child_b)

            population = next_population

        return None


    def greedy_plus_ga(
        graph: Graph,
        pop_size: int = 60,
        generations: int = 300,
        mutation_rate: float = 0.03,
        rng_seed: int = 42,
    ) -> Coloring:
        random.seed(rng_seed)

        best_coloring = greedy_coloring(graph)
        best_color_limit = num_colors(best_coloring)
        print(f"Initial Greedy coloring used k={best_color_limit}")

        for color_limit in range(best_color_limit - 1, 0, -1):
            print(f"Searching for feasible coloring with k={color_limit}...")
            candidate = ga_find_feasible_k(
                graph=graph,
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

    return (
        Coloring,
        Graph,
        List,
        Optional,
        conflict_count,
        greedy_coloring,
        greedy_plus_ga,
        num_colors,
        random,
    )


@app.cell
def _(conflict_count, graph, greedy_plus_ga, num_colors):
    if __name__ == "__main__":
        # 1. Define your graph (Adjacency List format)
        # This example is a small graph where nodes 0, 1, 2, 3 form a complete 
        # graph (K4) requiring 4 colors, and node 4 is attached to node 2.

        print("Starting Graph Coloring Meta-Heuristic...")

        # 2. Call the main runner function
        best_solution = greedy_plus_ga(
            graph=graph,
            pop_size=60,           # Size of the GA population
            generations=200,       # Number of iterations per k-color search
            mutation_rate=0.05,    # Probability of random color mutations
            rng_seed=42            # Seed for reproducibility
        )

        # 3. Output the final results
        if best_solution:
            print("\n--- Final Results ---")
            print("Best Coloring Found:", best_solution)
            print("Total Colors Used:", num_colors(best_solution))
            print("Remaining Conflicts:", conflict_count(graph, best_solution))
        else:
            print("\nNo valid coloring could be found.")
    return


@app.cell
def _(solution):
    max((value for key, value in solution.items()))
    return


@app.cell
def _(conflict_count, graph, greedy_coloring, num_colors, solution):
    greedy_solution = greedy_coloring(graph)

    conflict_count(graph, greedy_solution), conflict_count(graph, solution), num_colors(greedy_solution), num_colors(solution)
    return


@app.cell
def _(Coloring, Graph, List, Optional, random):
    class GraphColoringHeuristic:
        def __init__(self, graph: Graph, rng_seed: int = 42) -> None:
            self.graph = graph
            self.rng = random.Random(rng_seed)

        def greedy_coloring(self) -> Coloring:
            coloring: Coloring = {}
            for vertex in self.graph:
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

            for color_limit in range(best_color_limit - 1, 0, -1):
                candidate = self.ga_find_feasible_k(
                    initial_coloring=best_coloring,
                    color_limit=color_limit,
                    population_size=pop_size,
                    generation_count=generations,
                    mutation_probability=mutation_rate,
                    elite_count=2,
                )
                if candidate is None:
                    break

                best_coloring = candidate
                best_color_limit = color_limit

            return best_coloring

    return (GraphColoringHeuristic,)


@app.cell
def _(GraphColoringHeuristic, graph):
    solver = GraphColoringHeuristic(graph, rng_seed=42)
    solution = solver.greedy_plus_ga(pop_size=80, generations=400, mutation_rate=0.04)
    return (solution,)


if __name__ == "__main__":
    app.run()
