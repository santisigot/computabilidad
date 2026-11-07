# Trabajo Final — Teoría de la Computabilidad (2026)

**Título:** Análisis del Problema del Viajante (TSP): solución exacta vs. heurística  
**Carrera:** Licenciatura en Sistemas de Información  
**Integrantes:** Schenberger Felipe · Sigot Santiago · Mete Luigi  
**Problema elegido:** TSP (NP-difícil)

> Este documento es el borrador del informe entregable. Exportarlo a PDF o DOCX e incorporar los gráficos de `resultados/`.

---

## 1. Introducción

El Problema del Viajante (TSP) consiste en encontrar el recorrido de menor distancia que visita un conjunto de ciudades exactamente una vez y regresa al origen. Aparece en logística, transporte y planificación de recorridos.

Aunque el planteo es simple, encontrar la ruta óptima se vuelve inviable al crecer la cantidad de ciudades. Este trabajo compara:

1. un **algoritmo exacto** por fuerza bruta (óptimo, costo factorial);
2. una **heurística** del vecino más cercano (rápida, no garantiza optimalidad).

El caso base usa seis ciudades reales de Entre Ríos; para instancias mayores se agregan puntos sintéticos reproducibles (semilla 2026).

## 2. Definición del problema

Cada ciudad es un punto geográfico `(latitud, longitud)`. La distancia entre dos ciudades se calcula con **Haversine** (km en línea recta). Se asume TSP **simétrico**.

Objetivo: circuito que empiece en una ciudad, visite todas una sola vez, regrese al origen y minimice la distancia total.

## 3. Complejidad computacional

El TSP de optimización es **NP-difícil**. Fijando el origen, la fuerza bruta evalúa `(n − 1)!` recorridos. Ese crecimiento factorial explica por qué el exacto solo sirve para instancias pequeñas.

## 4. Algoritmo exacto (fuerza bruta)

Se fija la primera ciudad como origen y se enumeran todas las permutaciones del resto. Para cada circuito se suma la distancia (incluido el regreso) y se conserva el mínimo.

**Por qué es costoso:** la cantidad de rutas crece como `(n − 1)!`. El código acepta el parámetro `n` y un límite opcional de tiempo (3600 s = 1 h), alineado con la consigna.

Implementación: `ciudades.py`.

## 5. Heurística del vecino más cercano

Desde el origen, en cada paso se elige la ciudad no visitada más cercana; al final se regresa al inicio.

**Funcionamiento:** (1) fijar ciudad inicial; (2) mientras queden sin visitar, avanzar a la más cercana; (3) volver al origen.

- **Ventajas:** simple de implementar y explicar; complejidad O(n²); viable con n grandes (miles de ciudades en segundos).
- **Limitaciones:** es voraz (solo mira el siguiente paso); no garantiza optimalidad; puede dejar “ciudades lejanas” para el final y alargar el circuito.

Implementación: `heuristica.py`.

## 6. Metodología experimental

| Aspecto | Detalle |
|--------|---------|
| Lenguaje | Python 3 |
| Distancias | Haversine (km) |
| Instancias | Semilla 2026; n≤6 ciudades reales de Entre Ríos; n>6 puntos sintéticos en la región |
| Medición | `time.perf_counter()` |
| Condiciones | Misma máquina; mismos casos para exacto y heurística |
| Límite exacto | 3600 s (1 hora) |
| Error relativo | `((d_heur − d_opt) / d_opt) × 100` |

Comando:

```bash
pip install -r requirements.txt
python experimentos.py
python graficar.py
```

## 7. Resultados

### 7.1 Comparación exacto vs. heurística (punto 6)

Mismos casos para ambos algoritmos (semilla 2026).

| n | Recorridos exactos | Tiempo exacto (s) | Dist. óptima (km) | Tiempo heur. (s) | Dist. heur. (km) | Error (%) |
|---|--------------------|-------------------|-------------------|------------------|------------------|-----------|
| 6 | 120 | 0.00005 | 675.60 | 0.00003 | 885.40 | 31.05 |
| 7 | 720 | 0.00032 | 723.92 | 0.00003 | 933.72 | 28.98 |
| 8 | 5040 | 0.00238 | 724.21 | 0.00005 | 884.78 | 22.17 |
| 9 | 40320 | 0.02039 | 777.59 | 0.00007 | 938.17 | 20.65 |
| 10 | 362880 | 0.20213 | 801.66 | 0.00007 | 962.23 | 20.03 |
| 11 | 3628800 | 2.24588 | 883.76 | 0.00008 | 920.92 | 4.20 |
| 12 | 39916800 | 25.32610 | 885.24 | 0.00009 | 1045.82 | 18.14 |
| 13 | 479001600 | 324.09527 | 888.20 | 0.00012 | 1048.78 | 18.08 |
| 14 | 6227020800 | **> 3600 (corte 1 h)** | — | — | — | — |

**Punto 3 (límite 1 hora):** n=13 completa en ~324 s. n=14 se corta al superar 1 hora (proyección ≈ 4213 s ≈ 1,17 h). Ahí termina el barrido del exacto.

**Respuestas directas de la consigna:**

- **¿Alcanzó el óptimo?** No: en todos los n medidos (6..13) el error relativo fue > 0 %.
- **Error relativo:** entre 4,20 % (n=11) y 31,05 % (n=6, ciudades reales).
- **Tiempo:** la heurística es órdenes de magnitud más rápida; en n=13 el exacto tarda ~324 s y la heurística ~0,0001 s.

### 7.2 Gráfico tiempo vs. n (punto 4)

Incluir `resultados/tiempos_vs_n.png` (eje Y logarítmico).

La curva del exacto crece de forma compatible con `(n−1)!`. La de la heurística permanece casi plana en esa escala. Eso confirma la complejidad teórica: factorial vs. polinomial O(n²).

### 7.3 Escalabilidad de la heurística (punto 7)

| n | Tiempo (s) | Distancia (km) |
|---|------------|----------------|
| 1000 | 0.64 | 9753.48 |
| 2000 | 2.73 | 13737.83 |
| 5000 | 16.96 | 21072.21 |

**¿Viable para casos reales?** Sí, como método rápido de construcción de rutas. Con miles de puntos responde en segundos. El exacto, en cambio, ya es poco práctico en n=13 (~5,4 min) y se proyecta que n=14 supera 1 hora. Incluir `resultados/escalabilidad_heuristica.png`.

## 8. Aplicación en contexto real (Entre Ríos)

**Caso:** planificación de recorridos de reparto / logística entre localidades (p. ej. Concepción del Uruguay, Colón, Gualeguaychú, Concordia, Paraná, Villaguay).

- **Modelado:** cada parada = ciudad; costo = distancia o tiempo de viaje; objetivo ≈ TSP (a veces con ventanas horarias o capacidad → VRP).
- **Impacto:** menos km → menor combustible, tiempo y costo operativo.
- **Práctica:** se usan heurísticas y metaheurísticas (vecino más cercano, 2-opt, genéticos, etc.) y herramientas de ruteo; la fuerza bruta no escala.

## 9. Conclusiones

1. El TSP ilustra un problema fácil de enunciar y duro de optimizar.
2. La fuerza bruta garantiza optimalidad pero solo es práctica para n pequeño.
3. El vecino más cercano ofrece rutas útiles en tiempos razonables, con error relativo variable.
4. En aplicaciones reales de la región, las heurísticas (o solvers especializados) son la opción viable.

## 10. Reflexión crítica

Las distancias en línea recta subestiman el costo real (rutas, sentido único, tráfico). Aun así, el experimento muestra con claridad el trade-off **calidad vs. tiempo** que motiva el uso de heurísticas en la industria.

---

## Anexo — Cómo reproducir

Ver `README.md`. Código documentado y resultados en `resultados/`.
