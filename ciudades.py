"""TSP exacto por fuerza bruta (Entre Ríos + instancias sintéticas).

Las distancias se calculan en kilómetros con la fórmula de Haversine.
El algoritmo recibe el tamaño de entrada n (cantidad de ciudades) y,
opcionalmente, una lista de ciudades o una semilla para generarlas.
"""

from __future__ import annotations

from itertools import permutations
from math import asin, cos, radians, sin, sqrt
from random import Random
from time import perf_counter


# Seis ciudades reales de Entre Ríos (nombre, latitud, longitud).
CIUDADES_BASE = [
    ("Concepcion del Uruguay", -32.48463, -58.23217),
    ("Colon", -32.22312, -58.14426),
    ("Gualeguaychu", -33.00777, -58.51836),
    ("Concordia", -31.39200, -58.01710),
    ("Parana", -31.73271, -60.52897),
    ("Villaguay", -31.86800, -59.02700),
]

# Alias para compatibilidad con el resto del proyecto.
CIUDADES = CIUDADES_BASE

RADIO_TIERRA_KM = 6371.0
SEMILLA_DEFAULT = 2026


def distancia_km(ciudad_a, ciudad_b):
    """Distancia aproximada en línea recta entre dos ciudades (Haversine)."""
    _, lat_a, lon_a = ciudad_a
    _, lat_b, lon_b = ciudad_b

    lat_a, lon_a, lat_b, lon_b = map(radians, (lat_a, lon_a, lat_b, lon_b))
    delta_lat = lat_b - lat_a
    delta_lon = lon_b - lon_a

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat_a) * cos(lat_b) * sin(delta_lon / 2) ** 2
    )
    angulo = 2 * asin(sqrt(a))
    return RADIO_TIERRA_KM * angulo


def matriz_distancias(ciudades):
    """Precalcula la matriz simétrica de distancias entre ciudades."""
    n = len(ciudades)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia_km(ciudades[i], ciudades[j])
            matriz[i][j] = d
            matriz[j][i] = d
    return matriz


def distancia_ruta(ruta, matriz=None):
    """Suma los tramos de la ruta e incluye el regreso a la ciudad inicial."""
    total = 0.0
    n = len(ruta)
    for i in range(n):
        a = ruta[i]
        b = ruta[(i + 1) % n]
        if matriz is None:
            total += distancia_km(a, b)
        else:
            # Si la ruta trae índices enteros, usarlos; si trae tuplas, buscar.
            if isinstance(a, int) and isinstance(b, int):
                total += matriz[a][b]
            else:
                total += distancia_km(a, b)
    return total


def crear_ciudades(n, semilla=SEMILLA_DEFAULT):
    """Construye una instancia de n ciudades.

    Usa las ciudades reales de Entre Ríos y completa con puntos sintéticos
    reproducibles dentro de la región aproximada de la provincia.
    """
    if n < 3:
        raise ValueError("Se necesitan al menos 3 ciudades.")

    if n <= len(CIUDADES_BASE):
        return list(CIUDADES_BASE[:n])

    resultado = list(CIUDADES_BASE)
    generador = Random(semilla)
    while len(resultado) < n:
        numero = len(resultado) + 1
        latitud = generador.uniform(-33.7, -30.2)
        longitud = generador.uniform(-60.8, -57.7)
        resultado.append((f"Punto sintetico {numero}", latitud, longitud))
    return resultado


class TimeoutExacto(Exception):
    """Se lanza cuando el algoritmo exacto supera el límite de tiempo."""


def resolver_tsp_exacto(ciudades, limite_segundos=None):
    """Enumera todos los recorridos fijando la primera ciudad como origen.

    Complejidad: O((n-1)!) rutas evaluadas. Por eso es computacionalmente
    costoso: al crecer n, el número de permutaciones crece factorialmente.

    Args:
        ciudades: lista de ciudades (tuplas nombre/lat/lon).
        limite_segundos: si se indica, corta la búsqueda al superar ese tiempo.

    Returns:
        (mejor_ruta, mejor_distancia, rutas_evaluadas, tiempo_segundos)
    """
    if len(ciudades) < 3:
        raise ValueError("Se necesitan al menos tres ciudades.")

    matriz = matriz_distancias(ciudades)
    n = len(ciudades)
    origen = 0
    restantes = list(range(1, n))
    mejor_ruta_idx = None
    mejor_distancia = float("inf")
    rutas_evaluadas = 0
    inicio = perf_counter()

    for orden in permutations(restantes):
        if limite_segundos is not None:
            if perf_counter() - inicio > limite_segundos:
                raise TimeoutExacto(
                    f"El algoritmo exacto superó {limite_segundos} s "
                    f"con n={n} tras evaluar {rutas_evaluadas} rutas."
                )

        # Distancia del circuito: origen -> orden -> origen
        total = 0.0
        actual = origen
        for siguiente in orden:
            total += matriz[actual][siguiente]
            actual = siguiente
        total += matriz[actual][origen]
        rutas_evaluadas += 1

        if total < mejor_distancia:
            mejor_distancia = total
            mejor_ruta_idx = (origen,) + orden

    tiempo = perf_counter() - inicio
    mejor_ruta = tuple(ciudades[i] for i in mejor_ruta_idx)
    return mejor_ruta, mejor_distancia, rutas_evaluadas, tiempo


def resolver_tsp_exacto_n(n, semilla=SEMILLA_DEFAULT, limite_segundos=None):
    """Resuelve el TSP exacto para una instancia de tamaño n."""
    ciudades = crear_ciudades(n, semilla=semilla)
    return resolver_tsp_exacto(ciudades, limite_segundos=limite_segundos)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="TSP exacto por fuerza bruta (parámetro n)."
    )
    parser.add_argument(
        "-n",
        type=int,
        default=len(CIUDADES_BASE),
        help="Cantidad de ciudades (default: 6 ciudades reales).",
    )
    parser.add_argument(
        "--limite",
        type=float,
        default=None,
        help="Límite de tiempo en segundos (ej.: 3600).",
    )
    args = parser.parse_args()

    try:
        ruta, kilometros, cantidad, tiempo = resolver_tsp_exacto_n(
            args.n, limite_segundos=args.limite
        )
    except TimeoutExacto as exc:
        print(exc)
        raise SystemExit(1) from exc

    print(f"Ciudades (n): {args.n}")
    print(f"Recorridos evaluados: {cantidad}  [= (n-1)!]")
    print(f"Tiempo: {tiempo:.6f} s")
    print("Mejor recorrido:")
    print(" -> ".join(ciudad[0] for ciudad in ruta + (ruta[0],)))
    print(f"Distancia total en línea recta: {kilometros:.2f} km")
