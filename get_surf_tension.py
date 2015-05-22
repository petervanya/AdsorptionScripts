#!/usr/bin/env python
"""
Analyse the surface tensions of various
spin configurations of Pt clusters w or w/o water

Usage:
    get_surf_tension.py <cluster> -e <e> [-d <d>] (--print | --save [--latex])
                        [--ext <ext>]

Arguments:
    <cluster>          Pt cluster, e.g. 9_10_9
Options:
    -d <d>,--dir <d>   Custom directory w input files (TODO)
    -e <e>,--eta <e>   Adsorption site, 1, 2 or 3
    --print            Print table on screen
    --save             Save table in ~/Platinum/Water/Outfiles
    --ext <ext>        File extension, e.g. "nosymm"
    --latex            Add latex formatting for output

pv278@cam.ac.uk, 07/04/15
"""
import numpy as np
from math import sqrt
import pandas as pd
from docopt import docopt
from iolib import read_table, print_table, save_table

def isfloat(value):
    """check if character is float"""
    try:
        float(value)
        return True
    except ValueError:
        return False

    
def parse_data(file):
    data = []
    f = open(file,"r")
    for line in f:
        data.append( line.rstrip("\n").split(" \t ") )
    f.close()
    return data


if __name__ == "__main__":
    args = docopt(__doc__,version=1.0)
#    print args

    cluster = args["<cluster>"]
    eta = int(args["--eta"])
    ext = args["--ext"]

    home_dir = "/home/pv278"
    indir_p = home_dir + "/Platinum/Plain/Outfiles"
    indir_w = home_dir + "/Platinum/Water/Outfiles"
    fin = "Pt" + cluster + "_summary.out"
    inpath_p = indir_p + "/" + fin
    inpath_w = indir_w + "/" + fin

    Ewater = -76.393551              # ZP corrected B3LYP/LANL2DZ
    a = 2.775
    S = a**2*sqrt(3.0)/2.0*1e-20     # in m**2
    Nspins = 11
    spin_list = range(Nspins)
    
#    names = ["spin", "converged", "E", "cycles", "error", "time"]
    Ap = pd.read_table(inpath_p, header=None, index_col=False)
    if ext:
        path += "." + ext
    Aw = pd.read_table(inpath_w, sep="\t", header=None) #.ix[Nspins*(eta-1) : Nspins*eta] BROKEN!

    res = pd.DataFrame(columns=["energy (eV)", "SurfTension (J/m**2)"])
    for i in spin_list:
        Ep = Ap.ix[i][2]
        Ew = Aw.ix[i][6]
        if pd.notnull(Ew) and pd.notnull(Ep):
            dE = float(Ew) - Ewater - float(Ep)
            dE *= 27.21138505
            res.loc[spin_list[i]] = [dE, dE*1.602e-19/S]
    
    if args["--print"]:
         print res
    if args["--save"]:
        fout = "Pt" + cluster + "_E" + str(eta) + "_sigma.out"
        outpath = outdir + "/" + fout
        if args["--ext"]:
            outpath += "." + ext
        if args["--latex"]:
            res.to_latex(outpath)
        else:
            res.to_csv(outpath, sep="\t")
    
    
