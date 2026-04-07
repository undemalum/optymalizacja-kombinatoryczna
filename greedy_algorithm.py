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
    return


if __name__ == "__main__":
    app.run()
