import time
import random

def wczytaj_dowolny_graf(nazwa_pliku):
    krawedzie = []
    with open(nazwa_pliku, 'r') as f:
        for linia in f:
            linia = linia.strip()
            if not linia or linia.startswith('c') or linia.startswith('%'):
                continue
            czesci = linia.split()

            if czesci[0] == 'p':
                continue

            if len(czesci) == 3 and czesci[0].lower() == 'e':
                u, v = int(czesci[1]) - 1, int(czesci[2]) - 1
                krawedzie.append((u, v))

            elif len(czesci) >= 2 and czesci[0].isdigit() and czesci[1].isdigit():
                if len(krawedzie) == 0 and int(czesci[1]) > 5000:
                    continue
                u, v = int(czesci[0]) - 1, int(czesci[1]) - 1
                krawedzie.append((u, v))

    liczba_wierzcholkow = 0
    for u, v in krawedzie:
        if u > liczba_wierzcholkow: liczba_wierzcholkow = u
        if v > liczba_wierzcholkow: liczba_wierzcholkow = v
    liczba_wierzcholkow += 1

    graf = {i: set() for i in range(liczba_wierzcholkow)}
    for u, v in krawedzie:
        graf[u].add(v)
        graf[v].add(u)
    return graf


def welsh_powell(graf):
    kolory = {}
    for wierzcholek in range(len(graf)):
        zajete_kolory = {kolory[sasiad] for sasiad in graf[wierzcholek] if sasiad in kolory}
        kolor = 1
        while kolor in zajete_kolory:
            kolor += 1
        kolory[wierzcholek] = kolor
    return kolory

def ga_kolorowanie(graf, poczatkowe_kolory, max_iter, ga_dlugosc, max_czas):
    najlepsze_poprawne = poczatkowe_kolory.copy()
    obecne_k = max(najlepsze_poprawne.values())
    czas_start = time.perf_counter()
    n = len(graf)

    def buduj_conflict_count(kolory):
        cc = [0] * n
        for u in range(n):
            kol_u = kolory[u]
            for v in graf[u]:
                if kolory[v] == kol_u:
                    cc[u] += 1
        return cc

    while True:
        if time.perf_counter() - czas_start > max_czas:
            break

        docelowe_k = obecne_k - 1
        obecne_kolory = list(najlepsze_poprawne[i] for i in range(n))

        wierzcholki_do_zmiany = [w for w in range(n) if obecne_kolory[w] == obecne_k]
        for w in wierzcholki_do_zmiany:
            obecne_kolory[w] = random.randint(1, docelowe_k)

        cc = buduj_conflict_count(obecne_kolory)
        lista_ga = {}
        iteracja = 0
        znaleziono_poprawne = False
        iteracje_bez_poprawy = 0
        ostatnie_konflikty = sum(1 for x in cc if x > 0)

        while iteracja < max_iter:
            if time.perf_counter() - czas_start > max_czas:
                return najlepsze_poprawne

            konfliktowe = [u for u in range(n) if cc[u] > 0]

            if not konfliktowe:
                znaleziono_poprawne = True
                break

            iteracje_bez_poprawy += 1
            if iteracje_bez_poprawy > 200:
                for _ in range(max(1, n // 10)):
                    w = random.choice(konfliktowe)
                    obecne_kolory[w] = random.randint(1, docelowe_k)
                cc = buduj_conflict_count(obecne_kolory)
                lista_ga.clear()
                iteracje_bez_poprawy = 0
                continue

            najlepszy_ruch = None
            najlepsze_delta = float('inf')

            kandydaci = konfliktowe if len(konfliktowe) <= 50 else random.sample(konfliktowe, 50)

            for w in kandydaci:
                stary_kolor = obecne_kolory[w]
                konflikty_w_przed = sum(1 for v in graf[w] if obecne_kolory[v] == stary_kolor)

                for nowy_kolor in range(1, docelowe_k + 1):
                    if nowy_kolor == stary_kolor:
                        continue

                    ga_key = (w, nowy_kolor)
                    is_ga = (ga_key in lista_ga and lista_ga[ga_key] > iteracja)

                    konflikty_po = sum(1 for v in graf[w] if obecne_kolory[v] == nowy_kolor)
                    delta = konflikty_po - konflikty_w_przed

                    total_po = sum(1 for x in cc if x > 0) + delta
                    if is_ga and total_po >= 0:
                        continue

                    if delta < najlepsze_delta:
                        najlepsze_delta = delta
                        najlepszy_ruch = (w, stary_kolor, nowy_kolor)

            if najlepszy_ruch is None:
                break

            w, stary_kolor, nowy_kolor = najlepszy_ruch

            for v in graf[w]:
                if obecne_kolory[v] == stary_kolor:
                    cc[w] -= 1
                    cc[v] -= 1
                if obecne_kolory[v] == nowy_kolor:
                    cc[w] += 1
                    cc[v] += 1

            obecne_kolory[w] = nowy_kolor

            faktyczna_dlugosc = ga_dlugosc + random.randint(-ga_dlugosc // 10, ga_dlugosc // 10)
            lista_ga[(w, stary_kolor)] = iteracja + max(1, faktyczna_dlugosc)

            nowe_konflikty = sum(1 for x in cc if x > 0)
            if nowe_konflikty < ostatnie_konflikty:
                iteracje_bez_poprawy = 0
                ostatnie_konflikty = nowe_konflikty

            iteracja += 1

        if znaleziono_poprawne:
            najlepsze_poprawne = {i: obecne_kolory[i] for i in range(n)}
            obecne_k = docelowe_k
        else:
            break

    return najlepsze_poprawne


# 4. WYNIKI (Minimalistyczna Tabela)

if __name__ == "__main__":
    instancje = [
        "queen6.txt",
        "miles250.txt",
        "gc500.txt",
        "gc1000.txt",
        "le450_5a.txt"
    ]

    GA_DLUGOSC = 30
    LIMIT_CZASOWY = 180

    print(f"{'Instancja':<15} {'GA':<10} {'Czas (s)':<10}")

    for plik in instancje:
        try:
            graf = wczytaj_dowolny_graf(plik)
        except FileNotFoundError:
            print(f"| Brak pliku {plik}. Pomijam...{'':<30}|")
            continue

        # FAZA 1: Zachłanny
        wynik_zachlanny = welsh_powell(graf)
        kolory_startowe = max(wynik_zachlanny.values())

        # FAZA 2: GA (Genetic Algorithm)
        start_ga = time.perf_counter()
        wynik_koncowy = ga_kolorowanie(
            graf,
            wynik_zachlanny,
            max_iter=7500,
            ga_dlugosc=GA_DLUGOSC,
            max_czas=LIMIT_CZASOWY
        )
        czas_wykonania = time.perf_counter() - start_ga
        kolory_koncowe = max(wynik_koncowy.values())

        print(f"{plik:<15} {kolory_koncowe:<10} {czas_wykonania:<10.2f}")
