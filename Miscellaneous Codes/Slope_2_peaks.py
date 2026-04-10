import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

#read
def read_rad(filename):
    with open(filename, 'r') as f:
        f.readline()
        f.readline()
        f.readline()
        rad = []
        for line in f:
            l = line.split()
            rad.append(float(l[0]))
    return np.array(rad)


#parser
parser = argparse.ArgumentParser(description="Compute Gaussian widths vs file index")
parser.add_argument("-d", "--directory", required=True,
                    help="Folder containing dist_*.plt files")
parser.add_argument("-o", "--output", help="Output image filename")
args = parser.parse_args()

#For each dist
files = []
indices = []

for i in range(1,26):   # dist_0.plt hasta dist_25.plt
    fname = os.path.join(args.directory, f"dist_{i}.plt")
    if os.path.exists(fname):
        files.append(fname)
        indices.append(i)

if len(files) == 0:
    raise RuntimeError("No dist_*.plt files found.")

#GMM fit y guardar anchos
sigma1_list = []
sigma2_list = []

for file in files:

    rad = read_rad(file)
    rad = rad[np.isfinite(rad)]

    X = rad.reshape(-1, 1)

    gmm = GaussianMixture(n_components=2, random_state=0)
    gmm.fit(X)

    means = gmm.means_.flatten()
    sigmas = gmm.covariances_.flatten()

    # Ordenar por centro 
    order = np.argsort(means)

    sigma1_list.append(sigmas[order[0]])
    sigma2_list.append(sigmas[order[1]])

sigma1_list = np.array(sigma1_list)
sigma2_list = np.array(sigma2_list)
indices = np.array(indices)

#plot
fig, ax = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

ax[0].plot(indices[5:], sigma1_list[5:], 'o-',color="orange")
ax[0].set_ylabel(r'$\sigma_1$')
ax[0].set_title('Varianza distribución izquierda')
ax[0].set_ylim(0 ,1.2*np.max(sigma1_list))


ax[1].plot(indices[5:], sigma2_list[5:], 'o-')
ax[1].set_ylabel(r'$\sigma_2$')
ax[1].set_xlabel('Paso temporal')
ax[1].set_title('Varianza distribución derecha')


plt.tight_layout()

if args.output:
    plt.savefig(args.output, dpi=300)

#plt.show()
