import numpy as np
from scipy import stats
import argparse
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib as mpl

def read_data(indir):
    f = open(indir, 'r')
    f.readline()  # skip header

    tim = []
    rad_dev = []
    rad_skw = []
    rad_fla = []

    for line in f:
        L = line.split()
        try:
            t  = float(L[0])
            rd = float(L[1])
            rs = float(L[4])
            rf = float(L[7])
        except (ValueError, IndexError):
            continue

        if not (np.isfinite(t) and np.isfinite(rd)
                and np.isfinite(rs) and np.isfinite(rf)):
            continue

        tim.append(t)
        rad_dev.append(rd)
        rad_skw.append(rs)
        rad_fla.append(rf)

    f.close()

    return (
        np.array(tim),
        np.array(rad_dev),
        np.array(rad_skw),
        np.array(rad_fla)
    )

# ARGUMENTOS
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input-file',nargs='+',required=True,
    help='input file')
parser.add_argument('-o','--output-file',
    help='output file')
parser.add_argument('-N','--legend-name',nargs='+',
    help='legend names')
parser.add_argument('-s','--show-plot',action="store_true",
    help='show_plot')
args = parser.parse_args()

print("moments plot...")

# CONFIGURACIÓN DE GRÁFICAS
plt.style.use("seaborn-v0_8-whitegrid")
params = {'axes.labelsize' : 'large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large'}
pylab.rcParams.update(params)

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(6, 8))

ls_list = ['-','--',':']

label_list = []
if args.legend_name:
    label_list = args.legend_name
else:
    label_list = ["fit"] * len(args.input_file)


# LOOP PRINCIPAL
for i, infile in enumerate(args.input_file):

    tim, rad_dev, rad_skw, rad_fla = read_data(infile)
    x_new = tim * 1000.0  # ms

    # 1)  FIT LINEAL del ancho
    ax[0].plot(x_new, rad_dev, alpha=0.5)

    mask_dev = np.isfinite(x_new) & np.isfinite(rad_dev)
    x_dev = x_new[mask_dev]
    y_dev = rad_dev[mask_dev]

    if x_dev.size >= 2:
        coef = np.polyfit(x_dev, y_dev, 1)
        fit = np.poly1d(coef)

        x_fit = np.linspace(x_dev.min(), x_dev.max(), 1000)
        y_fit = fit(x_fit)

        y_pred = fit(x_dev)
        ss_res = np.sum((y_dev - y_pred) ** 2)
        ss_tot = np.sum((y_dev - np.mean(y_dev)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

        ax[0].plot(x_fit, y_fit,
            c='k', ls=ls_list[i % len(ls_list)], lw=2,
            label=label_list[i])

        eq_text = (
            f"$y = {coef[0]:.3e}x + {coef[1]:.3e}$\n"
            f"$R^2 = {r2:.3f}$"
        )
        ax[0].text(0.05, 0.95, eq_text,
                   transform=ax[0].transAxes,
                   fontsize=9, va='top',
                   bbox=dict(facecolor='white', alpha=0.7,
                             edgecolor='none'))

    ax[0].set_ylabel('$\langle \Delta r^2 \\rangle$')

    # 2) SKEWNESS – POLINOMIO 8
    ax[1].plot(x_new, rad_skw, alpha=0.5)

    mask_skw = np.isfinite(x_new) & np.isfinite(rad_skw)
    x_skw = x_new[mask_skw]
    y_skw = rad_skw[mask_skw]

    if x_skw.size >= 9:
        polyfit = np.polyfit(x_skw, y_skw, 8)
        fitting = np.poly1d(polyfit)

        x_fit = np.linspace(x_skw.min(), x_skw.max(), 1000)
        y_fit = fitting(x_fit)

        ax[1].plot(x_fit, y_fit,
            c='k', ls=ls_list[i % len(ls_list)], lw=2,
            label=label_list[i])

    ax[1].axhline(0, c='k', lw=2, ls='-.', alpha=0.5,
        label='$\\langle \\Delta r^3/\\sigma^3 \\rangle = 0$')
    ax[1].set_ylabel('$\langle \Delta r^3/\\sigma^3 \\rangle$')
    ax[1].legend()

    # 3) KURTOSIS – POLINOMIO 8
    ax[2].plot(x_new, rad_fla, alpha=0.5)

    mask_fla = np.isfinite(x_new) & np.isfinite(rad_fla)
    x_fla = x_new[mask_fla]
    y_fla = rad_fla[mask_fla]

    if x_fla.size >= 9:
        polyfit = np.polyfit(x_fla, y_fla, 8)
        fitting = np.poly1d(polyfit)

        x_fit = np.linspace(x_fla.min(), x_fla.max(), 1000)
        y_fit = fitting(x_fit)

        ax[2].plot(x_fit, y_fit,
            c='k', ls=ls_list[i % len(ls_list)], lw=2,
            label=label_list[i])


ax[0].legend()

ax[2].axhline(3, c='k', lw=2, ls='-.', alpha=0.5,
    label='$\\langle \\Delta r^4/\\sigma^4 \\rangle = 3$')
ax[2].set(
    xlabel="$t\\,(ms)$",
    ylabel='$\langle \Delta r^4/\\sigma^4 \\rangle$'
)
ax[2].xaxis.set_major_locator(plt.MaxNLocator(6))
ax[2].legend()

fig.tight_layout()
fig.subplots_adjust(hspace=0.1)


if args.output_file:
    plt.savefig(args.output_file, dpi=300, bbox_inches='tight')
if args.show_plot:
    plt.show()
