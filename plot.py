#!/usr/bin/env python
"""Usage:
    plot.py dos <cluster> [-s <s>]
    plot.py bandgap <cluster> 

Plot density of states for Pt atoms and storing figures
in Outfiles/Evals

Arguments:
    <cluster>           Pt cluster, e.g. 9_10_9

Options:
    -s <s>,--spin <s>   Spin state to plot

pv278@cam.ac.uk, 21/01/14
"""
import matplotlib.pyplot as plt
import numpy as np
import re
from docopt import docopt

def load_evals(fname, spin=0):
    return np.loadtxt(fname)

def load_evals_occ(fname, spin=0):
    return np.loadtxt(fname)

def plot_spin(E1, E2, fout):
    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    xmin = -20
    xmax = 20
    
    Bins=np.arange(xmin, xmax+1, 0.3)
    plt.hist(E1, bins=Bins, edgecolor="blue")
    plt.hist(E2, bins=Bins, color="red", edgecolor="red")
    
    plt.xlabel("$E$ (eV)")
    plt.ylabel("DoS")
    plt.xlim([xmin, xmax])
    plt.ylim([0, 50])
    spin = re.findall("S\d{1,2}", fout)[0][1:]
    plt.title("Density of states, $S$=" + spin)

    plt.savefig(fout)
    plt.close()
    print "Figure saved in", fout

def scatter_bandgap(cluster, dir):
    fin = dir + "Pt" + cluster + "_bandgap.out"
    A = np.loadtxt(fin)
    print A.shape
    spin = A[:,0]
    Eg = A[:,1]

    plt.scatter(spin, Eg)
    plt.xlabel("Spin")
    plt.ylabel("$E_{\\rm{gap}}$ (eV)")
    plt.title("Pt " + cluster)

    fout = fin.replace(".out", ".png")
    plt.savefig(fout)
    plt.close()
    print "Figure saved in",fout


if __name__ == "__main__":
    args = docopt(__doc__, version=1.0)
#    print args
    cluster = args["<cluster>"]
    base_dir = "/home/pv278/Platinum/Plain/Outfiles/Evals/"
    
    if args["dos"]:
        fin = base_dir + "evals_Pt" + cluster + ".out"
        fin_occ = base_dir + "evals_Pt" + cluster + "_occ.out"
        spin = args["--spin"]
    
        E = np.loadtxt(fin)
        Eocc = np.loadtxt(fin_occ)
        Ha = 27.211
        E, Eocc = E*Ha, Eocc*Ha      # conversion to eV
        
        if spin:
            spin_list = [spin]
        else:
            spin_list = range(11)
        
        for spin in spin_list:
            fout = fin.replace(".out", "_S" + str(spin) + ".png")
            plot_spin(E[:,spin], Eocc[:,spin], fout)

    if args["bandgap"]:
        scatter_bandgap(cluster, base_dir)


