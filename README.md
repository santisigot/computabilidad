# Trabajo Final 2026 — Teoría de la Computabilidad

**Problema:** TSP (Problema del Viajante) — NP-difícil  
**Integrantes:** Schenberger Felipe · Sigot Santiago · Mete Luigi  
**Enfoque:** fuerza bruta vs. vecino más cercano (ciudades de Entre Ríos).

## Requisitos

- Python 3.8+ (o superior).
- No requiere librerías externas (utiliza únicamente la biblioteca estándar de Python).

## Estructura

| Archivo / carpeta   | Rol                                                              |
| ------------------- | ---------------------------------------------------------------- |
| `exacto.py`         | Algoritmo exacto por fuerza bruta (`-n`, `--limite`)             |
| `heuristica.py`     | Heurística constructiva del vecino más cercano (`-n`)            |
| `comparar.py`       | Comparación puntual exacto vs. heurística sobre la misma muestra |
| `experimentos.py`   | Barrido de tiempos, generación de CSVs y prueba de escalabilidad |
| `resultados/`       | Carpeta generada por `experimentos.py` (tablas CSV y resumen)   |

Los PDF de la consigna están en `.gitignore` (no se versionan).

## Cómo ejecutar

```bash
# Ejecuciones individuales
python exacto.py -n 6
python heuristica.py -n 6
python comparar.py -n 6

# Experimentos (demo rápida n=6..10)
python experimentos.py --rapido

# Experimentos completos (hasta 1 h de límite para el exacto)
python experimentos.py
```

### Salidas de experimentos

Al ejecutar `experimentos.py`, se genera automáticamente el directorio `resultados/` con:
- `comparacion.csv`: tiempos, distancias y error relativo para cada valor de $n$.
- `escalabilidad_heuristica.csv`: tiempos y distancias para $n=1000$ y $n=2000$.
- `resultados.txt`: informe consolidado en texto plano.

## Presentación (20 min) — Guion

1. **Problema y relevancia:** planteo del TSP en Entre Ríos y cálculo de distancias (Haversine).
2. **Algoritmo exacto:** fuerza bruta y análisis de complejidad factorial `(n-1)!`.
3. **Explosión combinatoria:** análisis de tiempos de ejecución y límite de 1 h.
4. **Heurística del vecino más cercano:** enfoque voraz, complejidad $O(n^2)$ y límites de optimalidad.
5. **Comparación empírica:** relación entre tiempos de cómputo y error relativo.
6. **Escalabilidad ($n \ge 1000$):** viabilidad y rendimiento en instancias grandes.
7. **Conclusiones y cierre.**
