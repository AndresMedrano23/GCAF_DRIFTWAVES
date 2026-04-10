import os
import re
import argparse
import numpy as np
import pandas as pd
from scipy import stats

def read_mome(filepath, ycol=1):
    """Lee mome.plt y devuelve (tiempo_ms, y)."""
    times, ys = [], []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                t = float(parts[0])
                if len(parts) > ycol:
                    y = float(parts[ycol])
                else:
                    continue
            except ValueError:
                continue
            times.append(t)
            ys.append(y)
    times = np.array(times) * 1000.0  # convertir a ms
    return times, np.array(ys)


def fit_linear(x, y):
    """
    Ajuste lineal ignorando NaNs.
    Regresa: slope, r^2, t_final_ms
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # Mask finite values only
    mask = np.isfinite(x) & np.isfinite(y)
    x_fit = x[mask]
    y_fit = y[mask]

    # Need at least 2 points for a linear fit
    if x_fit.size < 2:
        return np.nan, np.nan, np.nan

    res = stats.linregress(x_fit, y_fit)
    slope = res.slope
    r2 = res.rvalue ** 2
    t_final = x_fit[-1]   # último tiempo realmente usado

    return slope, r2, t_final


def parse_dirname(dirname):
    """
    Extrae amplitude, r_position y n_waves de un nombre tipo:
    A10e5_R2_E1_n1_SUPER
    """
    a = re.search(r'A([^_]+)', dirname)
    r = re.search(r'R([^_]+)', dirname)
    n = re.search(r'n([^_]+)', dirname)

    amplitude = float(a.group(1)) if a else np.nan
    r_position = float(r.group(1)) if r else np.nan
    n_waves = int(n.group(1)) if n else np.nan

    return amplitude, r_position, n_waves


def main(mother_dir, out_file, ycol=1):
    rows = []

    for subdir in os.listdir(mother_dir):
        full_path = os.path.join(mother_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        mome_file = os.path.join(full_path, "mome.plt")
        if not os.path.exists(mome_file):
            continue

        # Extraer metadata
        amplitude, rpos, nwaves = parse_dirname(subdir)

        # Leer datos y ajustar
        t, y = read_mome(mome_file, ycol=ycol)
        slope, r2, t_final = fit_linear(t, y)

        rows.append({
            "amplitude": amplitude,
            "r_position": rpos,
            "n_waves": nwaves,
            "slope": slope,
            "r_squared": r2,
            "t_final_ms": t_final
        })

    df = pd.DataFrame(rows, columns=[
        "amplitude",
        "r_position",
        "n_waves",
        "slope",
        "r_squared",
        "t_final_ms"
    ])

    if out_file.lower().endswith(".xlsx"):
        df.to_excel(out_file, index=False)
    else:
        df.to_csv(out_file, index=False)

    print(f"Procesadas {len(df)} carpetas. Resultados guardados en {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Procesa subcarpetas con mome.plt y genera tabla."
    )
    parser.add_argument(
        "-i", "--input-dir",
        required=True,
        help="Carpeta madre"
    )
    parser.add_argument(
        "-o", "--output-file",
        default="results.csv",
        help="Archivo de salida (csv o xlsx)"
    )
    parser.add_argument(
        "--ycol",
        type=int,
        default=1,
        help="Columna Y a usar (0=tiempo, 1=rad_dev, etc.)"
    )

    args = parser.parse_args()
    main(args.input_dir, args.output_file, args.ycol)
