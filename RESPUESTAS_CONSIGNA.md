# Respuestas a la consigna — Trabajo Final 2026 (TSP)

**Integrantes:** Schenberger Felipe · Sigot Santiago · Mete Luigi  
**Problema:** TSP (NP-difícil) — ciudades de Entre Ríos + instancias sintéticas (semilla 2026)

Datos: `resultados/comparacion.csv`, `resultados/heuristica.csv`, gráficos en `resultados/`.

---

## 1. Selección del problema

Elegimos el **Problema del Viajante (TSP)**, NP-difícil de optimización: hallar el circuito de menor distancia que visita cada ciudad una vez y vuelve al origen.

---

## 2. Algoritmo exacto

**Implementación:** fuerza bruta en `ciudades.py`, parámetro `-n`.

Se fija la ciudad inicial y se evalúan todas las permutaciones del resto: **`(n − 1)!`** recorridos. Por eso es costoso: el trabajo crece de forma **factorial**.

Ejemplo: `python ciudades.py -n 6`

---

## 3. Experimentación del exacto (hasta > 1 hora)

Tiempos medidos (mismo hardware, instancias reproducibles):

| n | Recorridos `(n-1)!` | Tiempo exacto |
|---|---------------------|---------------|
| 6 | 120 | 0,00005 s |
| 7 | 720 | 0,00032 s |
| 8 | 5 040 | 0,00238 s |
| 9 | 40 320 | 0,02039 s |
| 10 | 362 880 | 0,202 s |
| 11 | 3 628 800 | 2,25 s |
| 12 | 39 916 800 | 25,3 s |
| 13 | 479 001 600 | **324,1 s (~5,4 min)** |
| 14 | 6 227 020 800 | **> 1 hora (corte / timeout)** |

**Conclusión punto 3:** el exacto es usable hasta n≈12–13. En **n=14** la ejecución **supera 1 hora** (proyectado ≈ 324 × 13 ≈ **4200 s ≈ 1,17 h**; la corrida se cortó al límite de la consigna). Ahí termina el barrido del algoritmo exacto.

---

## 4. Análisis gráfico

Gráfico: `resultados/tiempos_vs_n.png` (eje Y en escala **logarítmica**).

- **Eje X:** cantidad de ciudades `n`.  
- **Eje Y:** tiempo de ejecución (s).  
- La curva del **exacto** sube de forma abrupta (compatible con `(n−1)!`).  
- La de la **heurística** queda casi plana en esa escala.

**Interpretación:** cada ciudad extra multiplica el trabajo del exacto; la heurística apenas lo nota. Eso confirma la complejidad teórica factorial vs. polinomial O(n²).

---

## 5. Heurística

**Algoritmo:** vecino más cercano (`heuristica.py`).

1. Partir del origen.  
2. Ir siempre a la ciudad no visitada más cercana.  
3. Volver al origen.

| | |
|--|--|
| **Ventajas** | Simple, rápida, O(n²), sirve con n grandes |
| **Limitaciones** | Voraz; no garantiza óptimo; puede alargar el tramo final |

---

## 6. Comparación (mismos casos que el punto 3)

| n | Dist. óptima (km) | Dist. heur. (km) | Error relativo (%) | t exacto (s) | t heur. (s) |
|---|-------------------|------------------|--------------------|--------------|-------------|
| 6 | 675,60 | 885,40 | **31,05** | 0,00005 | 0,00003 |
| 7 | 723,92 | 933,72 | 28,98 | 0,00032 | 0,00003 |
| 8 | 724,21 | 884,78 | 22,17 | 0,00238 | 0,00005 |
| 9 | 777,59 | 938,17 | 20,65 | 0,020 | 0,00007 |
| 10 | 801,66 | 962,23 | 20,03 | 0,202 | 0,00007 |
| 11 | 883,76 | 920,92 | **4,20** | 2,25 | 0,00008 |
| 12 | 885,24 | 1045,82 | 18,14 | 25,3 | 0,00009 |
| 13 | 888,20 | 1048,78 | 18,08 | 324,1 | 0,00012 |

**Respuestas directas:**

1. **¿El heurístico alcanzó el óptimo?** No, en ninguno de los casos n=6..13 (error > 0 %).  
2. **Error relativo:** `((d_heur − d_opt) / d_opt) × 100` → entre **4,20 %** y **31,05 %**.  
3. **Tiempo:** la heurística es **órdenes de magnitud** más rápida (en n=13: ~324 s vs ~0,0001 s).

**Trade-off:** mejor calidad garantizada con el exacto, pero solo en n chico; la heurística sacrifica km a cambio de tiempo usable.

---

## 7. Escalabilidad del heurístico (n ≥ 1000)

| n | Tiempo | Distancia (km) |
|---|--------|----------------|
| 1000 | ~0,64 s | 9753 |
| 2000 | ~2,73 s | 13738 |
| 5000 | ~17 s | 21072 |

**¿Viable para casos reales?** Sí, como construcción rápida de rutas. Miles de puntos en segundos. El exacto no escala (n=14 > 1 h). El crecimiento observado es compatible con O(n²).

Gráfico: `resultados/escalabilidad_heuristica.png`.

---

## 8. Aplicación en contexto real (Entre Ríos)

**Caso:** logística / reparto entre localidades (Concepción del Uruguay, Colón, Gualeguaychú, Concordia, Paraná, Villaguay, etc.).

| Aspecto | Descripción |
|---------|-------------|
| **Modelado** | Cada parada = ciudad; costo = km o tiempo; el recorrido ≈ TSP (o VRP con varios vehículos/capacidad). |
| **Impacto** | Menos km → menos combustible, horas de chofer y demoras. Un error del ~30 % (como en n=6) sigue siendo caro a escala mensual. |
| **Práctica** | Heurísticas (vecino más cercano, 2-opt), OR-Tools, software de ruteo; casi nunca fuerza bruta. |

---

## 9. Informe — conclusiones para cerrar

1. El TSP es fácil de plantear y duro de optimizar.  
2. La fuerza bruta es óptima pero impropia para n grande (límite práctico ~13; n=14 > 1 h).  
3. El vecino más cercano da rutas útiles rápido, con error relativo variable (4–31 % aquí).  
4. En la región, lo realista son heurísticas / solvers, no enumeración total.

**Reflexión:** Haversine (línea recta) subestima el costo real (rutas, sentido único, tráfico), pero el experimento igual muestra con claridad el intercambio **calidad vs. tiempo**.

---

## Frases cortas para la oral (20 min)

1. *“Elegimos TSP porque es NP-difícil y aparece en logística entrerriana.”*  
2. *“El exacto prueba (n−1)! rutas: por eso a n=14 ya pasamos de una hora.”*  
3. *“El gráfico en escala log muestra la explosión factorial frente a la heurística casi plana.”*  
4. *“El vecino más cercano nunca pegó el óptimo en nuestros casos; el peor error fue 31 % en las 6 ciudades reales.”*  
5. *“Con 5000 puntos la heurística tarda ~17 s: viable; el exacto no.”*  
6. *“En la práctica se usan heurísticas y herramientas de ruteo, no fuerza bruta.”*

---

## Checklist entregable

- [x] Código documentado + README  
- [x] Exacto con parámetro `n` + límite 1 h  
- [x] Tabla de tiempos hasta el corte > 1 h (n=14)  
- [x] Gráfico n vs tiempo  
- [x] Heurística implementada y explicada  
- [x] Comparación calidad / error / tiempo  
- [x] Escalabilidad n≥1000  
- [x] Aplicación regional  
- [ ] Exportar `INFORME.md` (+ estas respuestas) a **PDF/DOCX** e insertar PNG  
- [ ] Diapositivas 20 min  
