"""Genera el gráfico n vs. tiempo (punto 4 de la consigna)."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


DIR_RESULTADOS = Path(__file__).resolve().parent / "resultados"
CSV_COMPARACION = DIR_RESULTADOS / "comparacion.csv"
CSV_ESCALABILIDAD = DIR_RESULTADOS / "escalabilidad_heuristica.csv"
GRAFICO_TIEMPOS = DIR_RESULTADOS / "tiempos_vs_n.png"
GRAFICO_ESCALABILIDAD = DIR_RESULTADOS / "escalabilidad_heuristica.png"


def _leer_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def graficar_comparacion(csv_path=CSV_COMPARACION, salida=GRAFICO_TIEMPOS):
    filas = _leer_csv(csv_path)
    ns = [int(f["n"]) for f in filas]
    t_exacto = [float(f["tiempo_exacto_s"]) for f in filas]
    t_heur = [float(f["tiempo_heuristica_s"]) for f in filas]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, t_exacto, "o-", label="Exacto (fuerza bruta)", color="#1f4e79")
    ax.plot(ns, t_heur, "s-", label="Heurística (vecino más cercano)", color="#c45911")
    ax.set_xlabel("Cantidad de ciudades (n)")
    ax.set_ylabel("Tiempo de ejecución (s)")
    ax.set_title("TSP: tiempo de ejecución vs. tamaño de entrada")
    ax.set_yscale("log")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida, dpi=150)
    plt.close(fig)
    print(f"Gráfico guardado en {salida}")


def graficar_escalabilidad(
    csv_path=CSV_ESCALABILIDAD, salida=GRAFICO_ESCALABILIDAD
):
    if not csv_path.exists():
        print(f"No se encontró {csv_path}; se omite el gráfico de escalabilidad.")
        return

    filas = _leer_csv(csv_path)
    ns = [int(f["n"]) for f in filas]
    tiempos = [float(f["tiempo_heuristica_s"]) for f in filas]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, tiempos, "o-", color="#548235")
    ax.set_xlabel("Cantidad de ciudades (n)")
    ax.set_ylabel("Tiempo de ejecución (s)")
    ax.set_title("Escalabilidad de la heurística del vecino más cercano")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida, dpi=150)
    plt.close(fig)
    print(f"Gráfico guardado en {salida}")


def main():
    parser = argparse.ArgumentParser(description="Genera gráficos del TP.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_COMPARACION,
        help="CSV de comparación exacto vs. heurística.",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        raise SystemExit(
            f"No existe {args.csv}. Ejecutá primero: python experimentos.py"
        )

    graficar_comparacion(args.csv)
    graficar_escalabilidad()


if __name__ == "__main__":
    main()
