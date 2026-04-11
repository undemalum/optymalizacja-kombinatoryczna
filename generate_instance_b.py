import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    graph_size = mo.ui.range_slider(
        start=400, stop=500, step=2, value=[400, 500]
    )
    graph_size
    return (graph_size,)


@app.cell
def _(graph_size):
    graph_size.value
    return


@app.cell
def _(graph_size):
    import random

    nodes = random.randint(graph_size.value[0], graph_size.value[1])
    nodes
    return nodes, random


@app.cell
def _(nodes, random):
    neighbors = {i: [] for i in range(nodes)}

    for node in range(nodes):
        attempts = random.randint(0, nodes - 1)

        for _ in range(attempts):
            neighbor = random.randint(0, nodes - 1)

            if node != neighbor and neighbor not in neighbors[node]:
                neighbors[node].append(neighbor)
                neighbors[neighbor].append(node)
                print(node, neighbor)
    return (neighbors,)


@app.cell
def _(neighbors):
    neighbors
    return


@app.cell
def _(mo):
    save = mo.ui.run_button("neutral", label="Save instance")
    save
    return (save,)


@app.cell
def _(mo, neighbors, nodes, save):
    mo.stop(not save.value)

    with open("instance.txt", "w") as f:
        f.write(str(nodes))
        for node_s, edges in neighbors.items():
            for edge in edges:
                f.write(f"{node_s} {edge}\n")
    return


if __name__ == "__main__":
    app.run()
