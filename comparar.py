from time import perf_counter

from ciudades import CIUDADES, resolver_tsp_exacto
from heuristica import vecino_mas_cercano
from ciudades import distancia_ruta


inicio = perf_counter()
ruta_optima, distancia_optima, recorridos = resolver_tsp_exacto(CIUDADES)
tiempo_exacto = perf_counter() - inicio

inicio = perf_counter()
ruta_heuristica = vecino_mas_cercano(CIUDADES)
distancia_heuristica = distancia_ruta(ruta_heuristica)
tiempo_heuristica = perf_counter() - inicio

error = ((distancia_heuristica - distancia_optima) / distancia_optima) * 100

print(f"Ciudades: {len(CIUDADES)}")
print(f"Recorridos exactos evaluados: {recorridos}")
print(f"Tiempo del algoritmo exacto: {tiempo_exacto:.8f} segundos")
print(f"Distancia óptima: {distancia_optima:.2f} km")
print(f"Tiempo de la heurística: {tiempo_heuristica:.8f} segundos")
print(f"Distancia de la heurística: {distancia_heuristica:.2f} km")
print(f"Error relativo: {error:.2f}%")