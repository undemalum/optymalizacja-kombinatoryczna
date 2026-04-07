import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import random

    nodes = random.randint(10, 100)
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


if __name__ == "__main__":
    app.run()
