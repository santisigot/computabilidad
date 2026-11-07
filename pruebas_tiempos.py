from random import Random
from time import perf_counter

from ciudades import CIUDADES, distancia_ruta, resolver_tsp_exacto
from heuristica import vecino_mas_cercano


def crear_ciudades_prueba(cantidad):
    if cantidad <= len(CIUDADES):
        return CIUDADES[:cantidad]

    resultado = list(CIUDADES)
    generador = Random(2026)

    while len(resultado) < cantidad:
        numero = len(resultado) + 1
        latitud = generador.uniform(-33.7, -30.2)
        longitud = generador.uniform(-60.8, -57.7)
        resultado.append(
            (f"Punto sintetico {numero}", latitud, longitud)
        )

    return resultado


print("n, recorridos exactos, tiempo exacto (s), tiempo heuristica (s), error (%)")

for n in range(6, 10):
    ciudades = crear_ciudades_prueba(n)

    inicio = perf_counter()
    ruta_optima, distancia_optima, recorridos = resolver_tsp_exacto(ciudades)
    tiempo_exacto = perf_counter() - inicio

    inicio = perf_counter()
    ruta_aproximada = vecino_mas_cercano(ciudades)
    distancia_aproximada = distancia_ruta(ruta_aproximada)
    tiempo_heuristica = perf_counter() - inicio

    error = (distancia_aproximada - distancia_optima) / distancia_optima * 100

    print(
        f"{n}, {recorridos}, {tiempo_exacto:.8f}, "
        f"{tiempo_heuristica:.8f}, {error:.2f}"
    )