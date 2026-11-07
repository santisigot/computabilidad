"""TSP exacto por fuerza bruta para seis ciudades de Entre Rios.

Las distancias se calculan en kilometros usando la formula de Haversine.
"""

from itertools import permutations
from math import asin, cos, radians, sin, sqrt


CIUDADES = [
    ("Concepcion del Uruguay", -32.48463, -58.23217),
    ("Colon", -32.22312, -58.14426),
    ("Gualeguaychu", -33.00777, -58.51836),
    ("Concordia", -31.39200, -58.01710),
    ("Parana", -31.73271, -60.52897),
    ("Villaguay", -31.86800, -59.02700),
]

RADIO_TIERRA_KM = 6371.0


def distancia_km(ciudad_a, ciudad_b):
    """Devuelve la distancia aproximada en linea recta entre dos ciudades."""
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


def distancia_ruta(ruta):
    """Suma los tramos de la ruta e incluye el regreso a la ciudad inicial."""
    total = 0.0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]
        total += distancia_km(ciudad_actual, ciudad_siguiente)
    return total


def resolver_tsp_exacto(ciudades):
    """Prueba todos los recorridos, fijando la primera ciudad como origen."""
    if len(ciudades) < 3:
        raise ValueError("Se necesitan al menos tres ciudades para este experimento.")

    origen = ciudades[0]
    restantes = ciudades[1:]
    mejor_ruta = None
    mejor_distancia = float("inf")
    rutas_evaluadas = 0

    for orden in permutations(restantes):
        ruta = (origen,) + orden
        total = distancia_ruta(ruta)
        rutas_evaluadas += 1

        if total < mejor_distancia:
            mejor_distancia = total
            mejor_ruta = ruta

    return mejor_ruta, mejor_distancia, rutas_evaluadas


if __name__ == "__main__":
    ruta, kilometros, cantidad = resolver_tsp_exacto(CIUDADES)

    print(f"Ciudades: {len(CIUDADES)}")
    print(f"Recorridos evaluados: {cantidad}")
    print("Mejor recorrido:")
    print(" -> ".join(ciudad[0] for ciudad in ruta + (ruta[0],)))
    print(f"Distancia total en linea recta: {kilometros:.2f} km")