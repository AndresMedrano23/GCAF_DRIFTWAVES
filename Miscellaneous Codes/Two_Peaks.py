import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns
from scipy.stats import norm
from sklearn.mixture import GaussianMixture

def read_data(indir):
    f = open(indir, 'r')
    f.readline()
    f.readline()
    rad, tht, zet, eng, pch = [], [], [], [], []
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
        return rf"${N}\pi/2$"
    else:
        return rf"${N//2}\pi$"



#Parser

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', required=True, help='input file')
parser.add_argument('-o', '--output-file', help='output file')
parser.add_argument('-t', '--type', required=True, help="plot type 'pos' or 'vel'")
parser.add_argument('-s', '--show-plot', action="store_true")
args = parser.parse_args()


#read data
rad, tht, zet, eng, pch = read_data(args.input_file)

#plot
sns.set_theme(style="whitegrid")
params = {
    'axes.labelsize': 'large',
    'xtick.labelsize': 'large',
    'ytick.labelsize': 'large'
}
pylab.rcParams.update(params)



#Position distributions


if args.type == 'pos':
    print("distribution plot pos...")
    fig, ax = plt.subplots(3, 1, figsize=(6, 6))

    # ---------- r/a histogram ----------
    rad_f = np.array(rad)
    rad_f = rad_f[np.isfinite(rad_f)]
    bins = 30
    sns.histplot(rad_f, bins=bins, stat="count",color="skyblue", ax=ax[0])

    # ----- Gaussian Mixture Model (2 populations) -----
    X = rad_f.reshape(-1, 1)
    #use teh GGM
    gmm = GaussianMixture(n_components=2, random_state=0)
    gmm.fit(X)
    # Extract the results
    weights = gmm.weights_
    means = gmm.means_.flatten()
    sigmas = np.sqrt(gmm.covariances_.flatten())

    xmin, xmax = ax[0].get_xlim()
    x = np.linspace(xmin, xmax, 400)

    bin_width = (xmax - xmin) / bins
    N = len(rad_f)
    #Plot the gaussian for each popualtion
    for i, (w, mu, s) in enumerate(zip(weights, means, sigmas)):
        pdf = w * norm.pdf(x, mu, s)
        ax[0].plot(
            x,
            pdf * N * bin_width,
            '--',
            linewidth=2,
            label=rf'Dist {i+1}: $\mu={mu:.3f}$, $\sigma={s:.3f}$'
        )
    #Labels
    ax[0].set_xlabel(r'$r/a$')
    ax[0].set_ylabel(r'$f(r/a)$')
    ax[0].legend()
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(7))
    ax[0].yaxis.set_major_locator(plt.MaxNLocator(4))

    # ---------- theta histogram ----------
    tht_f = np.array(tht)
    tht_f = tht_f[np.isfinite(tht_f)]

    ax[1].hist(tht_f, bins=20, density=True, alpha=0.5)
    ax[1].set_xlabel(r'$\theta$')
    ax[1].set_ylabel(r'$f(\theta)$')
    ax[1].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax[1].xaxis.set_major_formatter(plt.FuncFormatter(format_func))

    # ---------- zeta histogram ----------
    zet_f = np.array(zet)
    zet_f = zet_f[np.isfinite(zet_f)]

    ax[2].hist(zet_f, bins=20, density=True, alpha=0.5)
    ax[2].set_xlabel(r'$\zeta$')
    ax[2].set_ylabel(r'$f(\zeta)$')
    ax[2].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax[2].xaxis.set_major_formatter(plt.FuncFormatter(format_func))


plt.tight_layout()
# output
if args.output_file:
    plt.savefig(args.output_file)
if args.show_plot:
    plt.show()
