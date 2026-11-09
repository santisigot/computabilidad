"""Experimentos del trabajo final: tiempos, comparación y escalabilidad.

Punto 3: incrementa n hasta superar LIMITE_EXACTO_S (1 hora por defecto).
Punto 6: compara exacto vs. heurística en los mismos casos.
Punto 7: ejecuta la heurística con n grandes (por defecto 1000 y 2000).

Uso rápido (demo, n=6..10):
    python experimentos.py --rapido

Uso completo (hasta 1 h en el exacto):
    python experimentos.py
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from time import perf_counter

from exacto import TimeoutExacto, crear_ciudades, distancia_ruta, resolver_tsp_exacto
from heuristica import vecino_mas_cercano


LIMITE_EXACTO_S = 3600.0  # 1 hora, según la consigna
DIR_RESULTADOS = Path(__file__).resolve().parent / "resultados"
CSV_COMPARACION = DIR_RESULTADOS / "comparacion.csv"
CSV_ESCALABILIDAD = DIR_RESULTADOS / "escalabilidad_heuristica.csv"
TXT_RESUMEN = DIR_RESULTADOS / "resultados.txt"


def _escribir_csv(path, filas, campos):
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)


def correr_comparacion(n_valores, limite_segundos=LIMITE_EXACTO_S):
    """Puntos 3 y 6: exacto + heurística sobre las mismas instancias."""
    filas = []
    print(
        "n | recorridos | t_exacto (s) | dist_opt | "
        "t_heur (s) | dist_heur | error (%)",
        flush=True,
    )
    print("-" * 90, flush=True)

    for n in n_valores:
        print(f"Evaluando n={n}...", flush=True)
        ciudades = crear_ciudades(n)
        try:
            _, dist_opt, recorridos, t_exacto = resolver_tsp_exacto(
                ciudades, limite_segundos=limite_segundos
            )
        except TimeoutExacto as exc:
            print(f"\nTIMEOUT en n={n}: {exc}", flush=True)
            print(
                "Según la consigna, el experimento del exacto se detiene "
                "cuando una ejecución supera 1 hora.",
                flush=True,
            )
            break

        inicio = perf_counter()
        ruta_h = vecino_mas_cercano(ciudades)
        t_heur = perf_counter() - inicio
        dist_heur = distancia_ruta(ruta_h)
        error = ((dist_heur - dist_opt) / dist_opt) * 100

        fila = {
            "n": n,
            "recorridos_exactos": recorridos,
            "tiempo_exacto_s": round(t_exacto, 8),
            "distancia_optima_km": round(dist_opt, 4),
            "tiempo_heuristica_s": round(t_heur, 8),
            "distancia_heuristica_km": round(dist_heur, 4),
            "error_relativo_pct": round(error, 4),
        }
        filas.append(fila)
        print(
            f"{n:2d} | {recorridos:10d} | {t_exacto:12.6f} | "
            f"{dist_opt:8.2f} | {t_heur:10.6f} | {dist_heur:8.2f} | "
            f"{error:7.2f}",
            flush=True,
        )

    if filas:
        _escribir_csv(
            CSV_COMPARACION,
            filas,
            [
                "n",
                "recorridos_exactos",
                "tiempo_exacto_s",
                "distancia_optima_km",
                "tiempo_heuristica_s",
                "distancia_heuristica_km",
                "error_relativo_pct",
            ],
        )
        print(f"\nTabla guardada en {CSV_COMPARACION}")
    return filas


def correr_escalabilidad(n_valores=(1000, 2000)):
    """Punto 7: escalabilidad de la heurística con n grandes."""
    filas = []
    print("\nESCALABILIDAD DE LA HEURÍSTICA")
    print("n | tiempo (s) | distancia (km)")
    print("-" * 40)

    for n in n_valores:
        ciudades = crear_ciudades(n)
        inicio = perf_counter()
        ruta = vecino_mas_cercano(ciudades)
        tiempo = perf_counter() - inicio
        dist = distancia_ruta(ruta)
        fila = {
            "n": n,
            "tiempo_heuristica_s": round(tiempo, 6),
            "distancia_km": round(dist, 4),
        }
        filas.append(fila)
        print(f"{n:4d} | {tiempo:10.4f} | {dist:12.2f}")

    _escribir_csv(
        CSV_ESCALABILIDAD,
        filas,
        ["n", "tiempo_heuristica_s", "distancia_km"],
    )
    print(f"Tabla guardada en {CSV_ESCALABILIDAD}")
    return filas


def escribir_resumen(comparacion, escalabilidad):
    """Genera un resumen en texto para el informe."""
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    lineas = [
        "RESULTADOS DEL TRABAJO FINAL — TSP (Entre Ríos)",
        "=" * 60,
        "",
        "COMPARACIÓN EXACTO VS. HEURÍSTICA",
        "n | recorridos | t_exacto (s) | dist_opt | t_heur (s) | dist_heur | error (%)",
    ]
    for f in comparacion:
        lineas.append(
            f"{f['n']} | {f['recorridos_exactos']} | {f['tiempo_exacto_s']} | "
            f"{f['distancia_optima_km']} | {f['tiempo_heuristica_s']} | "
            f"{f['distancia_heuristica_km']} | {f['error_relativo_pct']}"
        )

    lineas.extend(
        [
            "",
            "ESCALABILIDAD DE LA HEURÍSTICA",
            "n | tiempo (s) | distancia (km)",
        ]
    )
    for f in escalabilidad:
        lineas.append(
            f"{f['n']} | {f['tiempo_heuristica_s']} | {f['distancia_km']}"
        )

    lineas.extend(
        [
            "",
            "Notas:",
            "- Instancias reproducibles con semilla 2026.",
            "- n<=6 usa ciudades reales de Entre Ríos; n>6 agrega puntos sintéticos.",
            "- Distancias en km (Haversine, línea recta).",
            f"- Límite del exacto: {LIMITE_EXACTO_S:.0f} s (1 hora).",
        ]
    )
    TXT_RESUMEN.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Resumen guardado en {TXT_RESUMEN}")


def main():
    parser = argparse.ArgumentParser(description="Experimentos del TP final.")
    parser.add_argument(
        "--rapido",
        action="store_true",
        help="Solo n=6..10 (para pruebas rápidas).",
    )
    parser.add_argument(
        "--hasta",
        type=int,
        default=13,
        help="Último n a intentar en el exacto (default: 13).",
    )
    parser.add_argument(
        "--desde",
        type=int,
        default=6,
        help="Primer n de la comparación (default: 6).",
    )
    parser.add_argument(
        "--limite",
        type=float,
        default=LIMITE_EXACTO_S,
        help="Límite en segundos para el exacto (default: 3600).",
    )
    parser.add_argument(
        "--escalabilidad",
        type=int,
        nargs="+",
        default=[1000, 2000],
        help="Valores de n para la heurística grande.",
    )
    args = parser.parse_args()

    if args.rapido:
        n_valores = list(range(6, 11))
        limite = args.limite
    else:
        n_valores = list(range(args.desde, args.hasta + 1))
        limite = args.limite

    print("Trabajo Final 2026 — Experimentos TSP")
    print(f"n a evaluar: {n_valores}")
    print(f"Límite exacto: {limite} s\n")

    comparacion = correr_comparacion(n_valores, limite_segundos=limite)
    escalabilidad = correr_escalabilidad(tuple(args.escalabilidad))
    escribir_resumen(comparacion, escalabilidad)


if __name__ == "__main__":
    main()
