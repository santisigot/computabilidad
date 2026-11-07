from ciudades import CIUDADES, distancia_km, distancia_ruta


def vecino_mas_cercano(ciudades):
    ruta = [ciudades[0]]
    sin_visitar = ciudades[1:]

    while sin_visitar:
        actual = ruta[-1]
        siguiente = min(
            sin_visitar,
            key=lambda ciudad: distancia_km(actual, ciudad)
        )
        ruta.append(siguiente)
        sin_visitar.remove(siguiente)

    return ruta


if __name__ == "__main__":
    ruta = vecino_mas_cercano(CIUDADES)
    distancia = distancia_ruta(ruta)

    print("Heurística del vecino más cercano")
    print("Ruta:")
    print(" -> ".join(ciudad[0] for ciudad in ruta + [ruta[0]]))
    print(f"Distancia total en línea recta: {distancia:.2f} km")