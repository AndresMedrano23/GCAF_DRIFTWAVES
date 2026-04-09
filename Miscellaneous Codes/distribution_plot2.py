import numpy as np

# definitions
def read_data(indir):  # read .plt data
    f = open(indir, 'r')
    f.readline()
    f.readline()
    rad = []
    tht = []
    zet = []
    eng = []
    pch = []
    f.readline()
    for line in f:
        l = line.split()
        rad.append(float(l[0]))
        tht.append(float(l[1]))
        zet.append(float(l[2]))
        eng.append(float(l[3]))
        pch.append(float(l[4]))
    f.close()
    return rad, tht, zet, eng, pch


def gaussian(x, t, dff, xm):
    return np.exp(-(x - xm) ** 2 / 4 / dff / t) / np.sqrt(4 * np.pi * dff * t)


def maxwellian(en):
    kt = 1
    return 2 * np.sqrt(en / np.pi) * (1 / kt) ** 1.5 * np.exp(-en / kt)


def format_func(value, tick_number):
    N = int(np.round(2 * value / np.pi))
    if N == 0:
        return "0"
    elif N == 1:
        return r"$\pi/2$"
    elif N == 2:
        return r"$\pi$"
    elif N == -1:
        return r"$-\pi/2$"
    elif N == -2:
        return r"$-\pi$"
    elif N % 2 > 0:
        return r"${0}\pi/2$".format(N)
    else:
        return r"${0}\pi$".format(N // 2)


# argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', required=True, help='input file')
parser.add_argument('-o', '--output-file', help='output file')
parser.add_argument('-t', '--type', help='plot type \'pos\' or \'vel\'', required=True)
parser.add_argument('-s', '--show-plot', action="store_true", help='show_plot')
args = parser.parse_args()

# plot
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
import seaborn as sns
from scipy.stats import norm

sns.set_theme(style="whitegrid")
params = {'axes.labelsize': 'large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large'}
pylab.rcParams.update(params)

rad, tht, zet, eng, pch = read_data(args.input_file)

if args.type == 'pos':
    print("distribution plot pos...")
    fig, ax = plt.subplots(3, 1, figsize=(6, 6))

    # --- r/a histogram ---
    rad_f = np.array(rad)[np.isfinite(rad)]
    sns.histplot(rad_f, ax=ax[0], bins=30, stat="count", kde=False, color="skyblue")

    mu, std = norm.fit(rad_f)
    xmin, xmax = ax[0].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    p_scaled = p * len(rad_f) * (xmax - xmin) / 30

    ax[0].plot(x, p_scaled, 'r--', label=f'N({mu:.2f}, {std:.2f})')
    ax[0].legend()
    ax[0].set_xlabel('$r/a$')
    ax[0].set_ylabel('$f(r/a)$')
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(7))
    ax[0].yaxis.set_major_locator(plt.MaxNLocator(4))

    # --- theta histogram ---
    tht_f = np.array(tht)[np.isfinite(tht)]
    ax[1].hist(tht_f, bins=20, density=True, alpha=0.5)
    ax[1].set_xlabel('$\\theta$')
    ax[1].set_ylabel('$f(\\theta)$')
    ax[1].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax[1].xaxis.set_major_formatter(plt.FuncFormatter(format_func))

    # --- zeta histogram ---
    zet_f = np.array(zet)[np.isfinite(zet)]
    ax[2].hist(zet_f, bins=20, density=True, alpha=0.5)
    ax[2].set_xlabel('$\\zeta$')
    ax[2].set_ylabel('$f(\\zeta)$')
    ax[2].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax[2].xaxis.set_major_formatter(plt.FuncFormatter(format_func))

if args.type == 'vel':
    print("distribution plot vel...")
    data = pd.DataFrame({'x': pch, 'y': eng}).dropna()
    with sns.axes_style('white'):
        plot = sns.jointplot(x='x', y='y', data=data, kind='scatter')
        plot.set_axis_labels("$\lambda$", "$\epsilon$(keV)")

plt.tight_layout()

# output
if args.output_file:
    plt.savefig(args.output_file)
if args.show_plot:
    plt.show()
