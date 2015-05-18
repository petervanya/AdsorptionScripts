#!/usr/bin/env python
"""
Analyse the surface tensions of various
spin configurations of Pt clusters w or w/o water

Usage:
    get_surf_tension.py <cluster> -e <e> [-d <d>] (--print | --save)
                        [--ext <ext>]

Arguments:
    <cluster>          Pt cluster, e.g. 9_10_9
Options:
    -d <d>,--dir <d>   Custom directory w input files (TODO)
    -e <e>,--eta <e>   Adsorption site, 1, 2 or 3
    --print            Print table on screen
    --save             Save table in ~/Platinum/Water/Outfiles
    --ext <ext>        File extension, e.g. "nosymm"

pv278@cam.ac.uk, 07/04/15
"""
from docopt import docopt
import numpy as np
from math import sqrt
from iolib import read_table, print_table, save_table

def isfloat(value):
    """check if character is float"""
    try:
        float(value)
        return True
    except ValueError:
        return False

#def print_table(res):
#    header = "Spin \t Energy (eV) \t Surf. tension (J/m**2)"
#    print header
#    print "-"*len(header)
#    N = len(res)
#    for i in range(N):
#        print res[i][0],'\t {0:.5f} \t {1:.5f}'.format(res[i][1],res[i][2])
    
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
    Pt_dir = "/home/pv278/Platinum"
    outdir = Pt_dir + "/Water/Outfiles"

    Ewater = -76.393551           # ZP corrected B3LYP/LANL2DZ
    a = 2.775
    S = a**2*sqrt(3.0)/2.0*1e-20  # in m**2
    Nspins = 11
    spins = range(Nspins)
    
    path = Pt_dir + "/Plain/Outfiles" + "/Pt" + cluster + "_summary.out"
    Aplain = read_table(path)
    path = outdir + "/Pt" + cluster + "_summary.out"
    if args["--ext"]:
        ext = args["--ext"]
        path += "." + ext
    Awater = read_table(path)[Nspins*(eta-1):Nspins*eta, :]

    res = []               # output table
    for i in spins:
        Ep = Aplain[i,2]   # plain Pt
        Ew = Awater[i,6]   # Pt with water
        if isfloat(Ew) and isfloat(Ep):
            dE = float(Ew) - Ewater - float(Ep)
            dE *= 27.21138505
            res.append([int(spins[i]), dE, dE*1.602e-19/S])
    
    res = np.matrix(res)
    
    if args["--print"]:
        print_table(res, "Spin \t Energy (eV) \t Surf. tension (J/m**2)")
    if args["--save"]:
        filename = outdir + "/Pt" + cluster + "_E" + str(eta) + "_sigma.out"
        if args["--ext"]:
            filename += "." + ext
        save_table(res, filename)
    
    
