# Trabajo Final 2026 — Teoría de la Computabilidad

**Problema:** TSP (Problema del Viajante) — NP-difícil  
**Integrantes:** Schenberger Felipe · Sigot Santiago · Mete Luigi  
**Enfoque:** fuerza bruta vs. vecino más cercano (ciudades de Entre Ríos).

## Requisitos

```bash
pip install -r requirements.txt
```

## Estructura

| Archivo / carpeta        | Rol                                       |
| ------------------------ | ----------------------------------------- |
| `exacto.py`              | Algoritmo exacto (parámetro `-n`)         |
| `heuristica.py`          | Vecino más cercano                        |
| `comparar.py`            | Comparación puntual exacto vs. heurística |
| `experimentos.py`        | Barrido de tiempos, CSV y escalabilidad   |
| `graficar.py`            | Gráficos n vs. tiempo                     |
| `INFORME.md`             | Informe del trabajo                       |
| `RESPUESTAS_CONSIGNA.md` | Respuestas a los puntos de la consigna    |
| `resultados/`            | Tablas, gráficos y resumen                |

Los PDF de la consigna están en `.gitignore` (no se suben).

## Cómo ejecutar

```bash
python exacto.py -n 6
python heuristica.py -n 6
python comparar.py -n 6

# Experimentos (demo rápida)
python experimentos.py --rapido

# Experimentos completos (exacto hasta 1 h)
python experimentos.py

# Gráficos
python graficar.py
```

## Presentación (20 min) — guion

1. Problema y relevancia (TSP / Entre Ríos)
2. Exacto y por qué cuesta `(n−1)!`
3. Gráfico de tiempos y límite de 1 h (n=14)
4. Heurística: ventajas y límites
5. Comparación: error relativo y tiempos
6. Escalabilidad n≥1000 y aplicación real
7. Conclusiones
