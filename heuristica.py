"""Heurística del vecino más cercano para el TSP.

Desde una ciudad inicial, en cada paso se avanza a la ciudad no visitada
más cercana. Al final se regresa al origen.

Ventajas: simple, rápida (O(n²)) y usable con n grandes.
Limitaciones: es voraz; decisiones locales pueden empeorar la ruta global
y no garantiza optimalidad.
"""

from __future__ import annotations

from time import perf_counter

from exacto import (
    CIUDADES,
    SEMILLA_DEFAULT,
    crear_ciudades,
    distancia_ruta,
    matriz_distancias,
)


def vecino_mas_cercano(ciudades):
    """Construye una ruta con la heurística del vecino más cercano."""
    if len(ciudades) < 3:
        raise ValueError("Se necesitan al menos tres ciudades.")

    matriz = matriz_distancias(ciudades)
    n = len(ciudades)
    visitado = [False] * n
    ruta_idx = [0]
    visitado[0] = True
    actual = 0

    for _ in range(n - 1):
        mejor = None
        mejor_dist = float("inf")
        for j in range(n):
            if not visitado[j] and matriz[actual][j] < mejor_dist:
                mejor_dist = matriz[actual][j]
                mejor = j
        ruta_idx.append(mejor)
        visitado[mejor] = True
        actual = mejor

    return [ciudades[i] for i in ruta_idx]


def vecino_mas_cercano_n(n, semilla=SEMILLA_DEFAULT):
    """Aplica la heurística a una instancia de tamaño n."""
    ciudades = crear_ciudades(n, semilla=semilla)
    inicio = perf_counter()
    ruta = vecino_mas_cercano(ciudades)
    tiempo = perf_counter() - inicio
    distancia = distancia_ruta(ruta)
    return ruta, distancia, tiempo


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Heurística del vecino más cercano para el TSP."
    )
    parser.add_argument(
        "-n",
        type=int,
        default=len(CIUDADES),
        help="Cantidad de ciudades (default: 6).",
    )
    args = parser.parse_args()

    ruta, distancia, tiempo = vecino_mas_cercano_n(args.n)
    print("Heurística del vecino más cercano")
    print(f"Ciudades (n): {args.n}")
    print(f"Tiempo: {tiempo:.6f} s")
    print("Ruta:")
    print(" -> ".join(ciudad[0] for ciudad in ruta + [ruta[0]]))
    print(f"Distancia total en línea recta: {distancia:.2f} km")
