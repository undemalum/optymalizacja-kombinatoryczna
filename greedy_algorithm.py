import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    return


@app.function
def read_graph(filename: str, undirected: bool = True) -> dict[int, set[int]]:
    from collections import defaultdict
    graph = defaultdict(set)

    with open(filename, "r") as f:
        next(f, None)
        for line in f:
            if not line.strip():
                continue

            u, v = map(int, line.split())
            graph[u].add(v)

            if undirected:
                graph[v].add(u)

    return graph


@app.cell
def _():
    # def read_graph(filename: str) -> dict[list[int]]:
    #     graph = {}
    #     with open(filename, "r") as f:
    #         _ = f.readline()
    #         for line in f:
    #             if not line.strip():
    #                 continue
    #             node, edge = list(map(int, line.split()))

    #             if not node in graph:
    #                 graph[node] = [edge]
    #             else:
    #                 graph[node].append(edge)
    #     return graph
    return


@app.function
def read_graph_no_duplicate(filename: str) -> dict[list[int]]:
    graph = {}
    with open(filename, "r") as f:
        _ = f.readline()
        for line in f:
            if not line.strip():
                continue

            node, edge = list(map(int, line.split()))

            if not node in graph:
                graph[node] = [edge]
                if not edge in graph:
                    graph[edge] = [node]
                else:
                    graph[edge].append(node)
            else:
                graph[node].append(edge)
                if not edge in graph:
                    graph[edge] = [node]
                else:
                    graph[edge].append(node)
    return graph


@app.cell
def _():
    graph = read_graph("gc_1000.txt", True)
    graph
    return (graph,)


@app.cell
def _(graph):
    coloring = {}

    for vertex in sorted(graph):
        color = 1

        neighbor_colors = {coloring[n] for n in graph[vertex] if n in coloring}
        while color in neighbor_colors:
            color += 1

        coloring[vertex] = color

    coloring
    return (coloring,)


@app.cell
def _(coloring):
    max((value for key, value in coloring.items()))
    #len(set(coloring.values()))
    return


if __name__ == "__main__":
    app.run()
