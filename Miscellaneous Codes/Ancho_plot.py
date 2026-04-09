import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


def read_data(indir):
    f = open(indir, 'r')
    f.readline()  # skip header

    tim = []
    rad_dev = []

    for line in f:
        L = line.split()
        try:
            t  = float(L[0])
            rd = float(L[1])
        except (ValueError, IndexError):
            continue

        if not (np.isfinite(t) and np.isfinite(rd)):
            continue

        tim.append(t)
        rad_dev.append(rd)

    f.close()

    return np.array(tim), np.array(rad_dev)


# ARGUMENTOS

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input-file', nargs='+', required=True,
    help='input file')
parser.add_argument('-o','--output-file',
    help='output file')
parser.add_argument('-N','--legend-name', nargs='+',
    help='legend names')
parser.add_argument('-s','--show-plot', action="store_true",
    help='show plot')
args = parser.parse_args()

print("linear fit plot...")


# CONFIGURACIÓN DE GRÁFICA

plt.style.use("seaborn-v0_8-whitegrid")
params = {'axes.labelsize' : 'large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large'}
pylab.rcParams.update(params)

fig, ax = plt.subplots(1, 1, figsize=(6, 5))

ls_list = ['-','--',':']

if args.legend_name:
    label_list = args.legend_name
else:
    label_list = ["fit"] * len(args.input_file)

# LOOP PRINCIPAL
for i, infile in enumerate(args.input_file):

    tim, rad_dev = read_data(infile)
    x_new = tim * 1000.0  # ms

    ax.plot(x_new, rad_dev, alpha=0.5)

    mask = np.isfinite(x_new) & np.isfinite(rad_dev)
    x = x_new[mask]
    y = rad_dev[mask]

    if x.size >= 2:
        coef = np.polyfit(x, y, 1)
        fit = np.poly1d(coef)

        x_fit = np.linspace(x.min(), x.max(), 1000)
        y_fit = fit(x_fit)

        y_pred = fit(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

        ax.plot(
            x_fit, y_fit,
            c='k', lw=2,
            ls=ls_list[i % len(ls_list)],
            label=label_list[i]
        )

        eq_text = (
            f"$y = {coef[0]:.3e}x + {coef[1]:.3e}$\n"
            f"$R^2 = {r2:.3f}$"
        )

        ax.text(
            0.05, 0.95, eq_text,
            transform=ax.transAxes,
            fontsize=9, va='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )


ax.set(
    xlabel="$t\\,(ms)$",
    ylabel='$\langle \Delta r^2 \\rangle$'
)
ax.legend()
ax.xaxis.set_major_locator(plt.MaxNLocator(6))

fig.tight_layout()


if args.output_file:
    plt.savefig(args.output_file, dpi=300, bbox_inches='tight')
if args.show_plot:
    plt.show()
