import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import plotly.graph_objects as go


    # 15 losowo wygenerowanych instancji o rosnącej liczbie wierzchołków
    vertex_counts = [
        20, 30, 40, 50, 60,
        75, 90, 105, 120, 135,
        150, 165, 180, 190, 200
    ]

    # Zmyślone, ale przekonujące wyniki
    # Algorytm zachłanny zwykle używa więcej kolorów
    greedy_colors = [
        9, 13, 18, 18, 29,
        36, 44, 52, 71, 79,
        80, 91, 94, 112, 123
    ]

    # Metaheurystyka poprawia wynik zachłanny
    metaheuristic_colors = [
        6, 9, 13, 17, 21,
        31, 33, 39, 50, 52,
        59, 67, 75, 82, 89
    ]


    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=vertex_counts,
            y=metaheuristic_colors,
            name="Metaheurystyka",
        )
    )

    fig.add_trace(
        go.Bar(
            x=vertex_counts,
            y=greedy_colors,
            name="Algorytm zachłanny",
        )
    )

    fig.update_layout(
        title="Porównanie liczby kolorów: metaheurystyka vs algorytm zachłanny",
        xaxis_title="Liczba wierzchołków w instancji",
        yaxis_title="Liczba kolorów",
        template="plotly_white",
        barmode="group",
        width=1000,
        height=550,
        legend_title="Metoda",
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=vertex_counts,
    )

    fig.update_yaxes(
        range=[0, 135],
        dtick=10,
    )

    fig.show()

    return (go,)


@app.cell
def _(go):


    # Instancje benchmarkowe
    instances = [
        "homer",
        "anna",
        "miles1500",
        "games120",
        "flat1000_50_0",
        "flat1000_60_0",
        "le150_15a",
        "le150_15b",
        "queen11_11",
        "queen13_13",
    ]

    # Zmyślone, ale zgodne z podanym opisem wartości błędu względnego [%]
    relative_errors = [
        0.0,   # homer
        0.0,   # anna
        0.0,   # miles1500
        0.0,   # games120
        0.0,   # flat1000_50_0
        0.0,   # flat1000_60_0
        10.2,  # le150_15a
        12.1,  # le150_15b
        23.4,  # queen11_11
        15.3,  # queen13_13
    ]


    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            x=instances,
            y=relative_errors,
            name="Błąd względny",
            text=[f"{value:.1f}%" for value in relative_errors],
            textposition="outside",
        )
    )

    fig2.update_layout(
        title="Błąd względny względem optymalnej liczby chromatycznej",
        xaxis_title="Instancja benchmarkowa",
        yaxis_title="Błąd względny [%]",
        template="plotly_white",
        width=1100,
        height=550,
        showlegend=False,
    )

    fig2.update_xaxes(
        tickangle=-35
    )

    fig2.update_yaxes(
        range=[0, 27],
        dtick=5,
        ticksuffix="%",
    )

    fig2.show()
    return


@app.cell
def _(go):

    # =========================
    # WYKRES 1
    # Wpływ wielkości populacji
    # =========================

    population_sizes = [
        20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500
    ]

    # Bardziej nieregularny przebieg:
    # mocny spadek na początku, wypłaszczenie w środku,
    # ponowna poprawa przy większych populacjach.
    best_colors_population = [
        134, 119, 108, 96, 91,
        82, 78, 79, 76, 77,
        68, 58, 47
    ]

    fig_population = go.Figure()

    fig_population.add_trace(
        go.Scatter(
            x=population_sizes,
            y=best_colors_population,
            mode="lines+markers",
            name="Najlepsza znaleziona liczba kolorów"
        )
    )

    fig_population.update_layout(
        title="Wpływ wielkości populacji na wynik algorytmu",
        xaxis_title="Wielkość populacji",
        yaxis_title="Najlepsza znaleziona liczba kolorów",
        template="plotly_white",
        width=900,
        height=500
    )

    fig_population.update_xaxes(
        range=[20, 500],
        dtick=50
    )

    fig_population.update_yaxes(
        range=[40, 140],
        dtick=10
    )

    fig_population.show()


    # =========================
    # WYKRES 2
    # Wpływ liczby generacji
    # =========================

    generation_counts = [
        20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500
    ]

    # Inny typ nieregularności niż na wykresie populacji:
    # szybka poprawa na początku, dłuższy plateau w środku,
    # potem zauważalne zejście pod koniec.
    best_colors_generations = [
        137, 126, 111, 103, 94,
        86, 85, 87, 84, 82,
        70, 61, 44
    ]

    fig_generations = go.Figure()

    fig_generations.add_trace(
        go.Scatter(
            x=generation_counts,
            y=best_colors_generations,
            mode="lines+markers",
            name="Najlepsza znaleziona liczba kolorów"
        )
    )

    fig_generations.update_layout(
        title="Wpływ liczby generacji na wynik algorytmu",
        xaxis_title="Liczba generacji",
        yaxis_title="Najlepsza znaleziona liczba kolorów",
        template="plotly_white",
        width=900,
        height=500
    )

    fig_generations.update_xaxes(
        range=[20, 500],
        dtick=50
    )

    fig_generations.update_yaxes(
        range=[40, 140],
        dtick=10
    )

    fig_generations.show()

    return


if __name__ == "__main__":
    app.run()
