import numpy as np
import matplotlib.pyplot as plt
import argparse
import os



#Parser
parser = argparse.ArgumentParser(
    description="Plot FTLE or log-separation from precomputed .dat files.")

parser.add_argument(
    "-i", type=str, required=True,
    help="Path to the .dat file (e.g. lyapunov_average_cart.dat)")

parser.add_argument(
    "-ftle", action="store_true",
    help="Plot FTLE evolution lambda(t)")

parser.add_argument(
    "-logsep", action="store_true",
    help="Plot logarithmic separation ln(sep)")

parser.add_argument(
    "-o", "--output", type=str, default=None,
    help="Base name for output PNG files (without extension)")

parser.add_argument(
    "-s", "--show", action="store_true",
    help="Show plots on screen")

parser.add_argument(
    "--plateau", type=float, default=0.65,
    help="Fraction of time series used as plateau (default: 0.65)")

args = parser.parse_args()

## Load file


data = np.loadtxt(args.i)
t = data[:, 0]
lambda_avg = data[:, 1]
sep_avg = data[:, 2]
lnsep = 5*np.log(sep_avg)


# Plateau region
p0 = int(args.plateau * len(t))

#stimates

lambda_est = np.median(lambda_avg[p0:])

#Now the collection of point of the upper value, let's take a period of 10 points

NP = 10
#number of full intevarls
n = len(lnsep)//NP

lnsepMAX = []
tMAX = []

for i in range(0, NP*n, NP):
    j = np.argmax(lnsep[i:i+NP])
    lnsepMAX.append(lnsep[i+j])
    tMAX.append(t[i+j])

lnsepMAX = np.array(lnsepMAX)
tMAX     = np.array(tMAX)


#stimation over plateau
coeffs = np.polyfit(tMAX[p0//NP:], lnsepMAX[p0//NP:], 1)
slope, intercept = coeffs

#name for saving

basename = os.path.splitext(os.path.basename(args.i))[0]
outbase = args.output if args.output else basename

## FTLE plot
if args.ftle:
    plt.figure(figsize=(8, 5))

    plt.plot(t, lambda_avg, lw=2, color="red",label=r"$\lambda(t)$ promedio")

    plt.axhline(lambda_est, color="black", ls="--",label=rf"Asintota $\lambda = {lambda_est:.3f}$")

    plt.xlabel("Tiempo [s]")
    plt.ylabel(r"$\lambda(t)\;[\mathrm{s}^{-1}]$")
    plt.title("Evolución del Exponente de Lyapunov a tiempo finito")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if args.output:
        fname = f"{outbase}_ftle.png"
        plt.savefig(fname, dpi=150)
        print(f"[Saved] {fname}")

#Separation

if args.logsep:
    plt.figure(figsize=(8, 5))

    plt.plot(t, lnsep, color="black", marker=".",label=r"$\ln(\langle \Delta(t) \rangle)$")
    #plt.plot(tMAX,lnsepMAX, color="red")
    plt.plot(tMAX[p0//NP:], slope * tMAX[p0//NP:] + intercept,"--",label=rf"Ajuste lineal $\lambda = {slope:.3f}$")
    plt.xlabel("Tiempo [s]")
    plt.ylabel(r"$\ln(\mathrm{sep})$")
    plt.title("Evolución logarítmica de la separación")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if args.output:
        fname = f"{outbase}_lnsep.png"
        plt.savefig(fname, dpi=150)
        print(f"[Saved] {fname}")
#show
if args.show:
    plt.show()
else:
    plt.close("all")