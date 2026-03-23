import marimo

__generated_with = "0.21.1"
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
    print(nodes)

    neighbors = {}
    for node in range(nodes):
        neighbors[node] = []
        for _ in range(random.randint(0, nodes)):
            neighbor = random.randint(0, nodes)

            if neighbor not in neighbors[node] and node not in neighbors.get(neighbor, []) and node != neighbor:
                neighbors[node].append(neighbor)
                print(node, neighbor)
    return


if __name__ == "__main__":
    app.run()
