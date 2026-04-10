import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input",required=True, help="File to process")
parser.add_argument("-t", "--type", help="ra o nw ")
parser.add_argument("-o", "--output", help="output name")
parser.add_argument("-s", "--show", action="store_true" )
args = parser.parse_args()



f = open(args.input)
f.readline()
rad , nw, slope = [], [], []
for line in f:
    l = line.split(",")
    rad.append(int(l[0]))
    nw.append(int(l[1]))
    slope.append(float(l[2]))
f.close()
rad = np.array(rad)
nw = np.array(nw)
slope = np.array(slope)



if args.type == "nw":
    ##Grafica pendiente vs NW
    RA = np.arange(2,10,1)
    for i in RA:
        mask = (rad == i)
        nw_mk = nw[mask]
        slope_mk = slope[mask]
        if len(nw_mk) > 1 :
            plt.plot(nw_mk, slope_mk, marker="o", label=f"r/a={i/10}")
    plt.title("Evolución de la pendiente contra número de ondas.")
    plt.xlabel("nw")
    plt.ylabel("Pendiente")
    plt.grid()
    plt.legend()
    if args.show:
        plt.show()
    else:
        plt.savefig(args.output)
elif args.type == "ra":

    ##Grafica Pendiente vs posición

    NWF = [1,2,5,10,20]

    for i in NWF:
        mask = (nw == i)
        rad_mk = rad[mask]
        slope_mk = slope[mask]
        if len(rad_mk) > 1:
            plt.plot(rad_mk/10, slope_mk, marker="o", label=f"nw={i}")
    plt.title("Evolución de la pendiente contra posición radial.")
    plt.xlabel("r/a")
    plt.ylabel("Pendiente")
    plt.grid()
    plt.legend()
    if args.show:
        plt.show()
    else:
        plt.savefig(args.output)

