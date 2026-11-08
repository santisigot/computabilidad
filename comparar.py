"""Comparación exacto vs. heurística sobre la misma instancia."""

from __future__ import annotations

import argparse
from time import perf_counter

from ciudades import crear_ciudades, distancia_ruta, resolver_tsp_exacto
from heuristica import vecino_mas_cercano


def comparar(n, semilla=2026, limite_segundos=None):
    """Compara ambos algoritmos sobre exactamente las mismas ciudades."""
    ciudades = crear_ciudades(n, semilla=semilla)

    ruta_optima, distancia_optima, recorridos, tiempo_exacto = resolver_tsp_exacto(
        ciudades, limite_segundos=limite_segundos
    )

    inicio = perf_counter()
    ruta_heuristica = vecino_mas_cercano(ciudades)
    tiempo_heuristica = perf_counter() - inicio
    distancia_heuristica = distancia_ruta(ruta_heuristica)

    error = ((distancia_heuristica - distancia_optima) / distancia_optima) * 100

    return {
        "n": n,
        "recorridos": recorridos,
        "tiempo_exacto": tiempo_exacto,
        "distancia_optima": distancia_optima,
        "ruta_optima": ruta_optima,
        "tiempo_heuristica": tiempo_heuristica,
        "distancia_heuristica": distancia_heuristica,
        "ruta_heuristica": ruta_heuristica,
        "error_relativo": error,
    }


def _imprimir(resultado):
    print(f"Ciudades: {resultado['n']}")
    print(f"Recorridos exactos evaluados: {resultado['recorridos']}")
    print(f"Tiempo del algoritmo exacto: {resultado['tiempo_exacto']:.8f} s")
    print(f"Distancia óptima: {resultado['distancia_optima']:.2f} km")
    print(
        "Ruta óptima: "
        + " -> ".join(c[0] for c in resultado["ruta_optima"] + (resultado["ruta_optima"][0],))
    )
    print(f"Tiempo de la heurística: {resultado['tiempo_heuristica']:.8f} s")
    print(f"Distancia de la heurística: {resultado['distancia_heuristica']:.2f} km")
    print(
        "Ruta heurística: "
        + " -> ".join(
            c[0] for c in resultado["ruta_heuristica"] + [resultado["ruta_heuristica"][0]]
        )
    )
    print(f"Error relativo: {resultado['error_relativo']:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compara fuerza bruta y vecino más cercano."
    )
    parser.add_argument("-n", type=int, default=6, help="Cantidad de ciudades.")
    parser.add_argument(
        "--limite",
        type=float,
        default=None,
        help="Límite de tiempo del exacto en segundos.",
    )
    args = parser.parse_args()
    _imprimir(comparar(args.n, limite_segundos=args.limite))
