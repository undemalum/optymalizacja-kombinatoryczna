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
        start=20, stop=500, step=1, value=[20, 500]
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
def _(random):
    def generate_instance(nodes: int) -> dict[int, list[int]]:
        neighbors = {i: [] for i in range(1, nodes + 1)}
    
        for node in range(1, nodes + 1):
            attempts = random.randint(0, nodes - 1)
    
            for _ in range(attempts):
                neighbor = random.randint(int(nodes / 4), nodes)
    
                if node != neighbor and neighbor not in neighbors[node]:
                    neighbors[node].append(neighbor)
                    neighbors[neighbor].append(node)
                    print(node, neighbor)
        return neighbors

    return (generate_instance,)


@app.cell
def _(generate_instance, nodes):
    neighbors = generate_instance(nodes)
    return (neighbors,)


@app.cell
def _(mo):
    save = mo.ui.run_button("neutral", label="Save instance")
    save
    return (save,)


@app.cell
def _(mo):
    filename = mo.ui.text()
    filename
    return (filename,)


@app.cell
def _(filename):
    filename.value
    return


@app.cell
def _(filename, mo, neighbors, nodes, save):
    mo.stop(not save.value)

    with open(f"{filename.value}.txt", "w") as f:
        f.write(str(nodes))
        for node_s, edges in neighbors.items():
            for edge in edges:
                f.write(f"{node_s} {edge}\n")
    return


if __name__ == "__main__":
    app.run()
