import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    graph = {}
    with open("instance.txt", "r") as f:
        for line in f:
            node, edge = list(map(int, line.split()))

            if not node in graph:
                graph[node] = [edge]
            else:
                graph[node].append(edge)

    graph
    return (graph,)


@app.cell
def _(graph):
    coloring = {}

    for vertex in graph:
        color = 0

        neighbor_colors = {coloring[n] for n in graph[vertex] if n in coloring}
        while color in neighbor_colors:
            color += 1

        coloring[vertex] = color

    coloring
    return


if __name__ == "__main__":
    app.run()
