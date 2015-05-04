#!/usr/bin/env python
"""
get_Pt_evals

Usage: get_Pt_evals.py -c <c> [-d <d>] [-h]

-h --help        Show this screen
-c c --cluster c Platinum cluster, e.g. 9_10_9
-d d --dir -d    Directory of evals file (default: ~/Platinum/Plain)

pv278@cam.ac.uk, 01/05/15
"""
from docopt import docopt
import numpy as np
import os
import itertools

def savedata(A,outfile):
    np.savetxt(outfile,A,"%.5f","\t")
    print "E-values printed in",outfile

# ===== read cmd ln args
args = docopt(__doc__)
#print args

home_dir = "/home/pv278/Platinum/"
cluster = args["<c>"]
if args["<d>"]:
    base_dir = home_dir + args["<d>"]
else:
    base_dir = home_dir + "Plain/"

# ===== check if necessary directories exist
outdir = "Outfiles/Evals"
if not os.path.exists(base_dir + outdir):
    os.makedirs(base_dir + outdir)
    print outdir,"created"

spin_list = range(11)
Nall = 44*sum([int(i) for i in cluster.split("_")])
Nocc = 18*sum([int(i) for i in cluster.split("_")])
Nvirt = Nall - Nocc
mat_all = np.zeros((Nall,len(spin_list)))
mat_occ = np.zeros((Nocc,len(spin_list)))

for i in spin_list:
    fname = base_dir+"Pt"+cluster+"/S_"+str(i)+"/Pt.out"
    gfile = open(fname).readlines()
 
    all = [line.split()[2:] for line in [l for l in gfile if "Eigenvalues" in l]]
    e_all = [float(eval) for eval in list(itertools.chain(*all))]
 
    occ = [line.split()[4:] for line in [l for l in gfile if "occ." in l]]
    e_occ = [float(eval) for eval in list(itertools.chain(*occ))]
    
    virt = [line.split()[4:] for line in [l for l in gfile if "virt." in l]]
    e_virt = [float(eval) for eval in list(itertools.chain(*virt))]
 
    if i == 0:              # double the e-values due to degeneracy
        e_all += e_all
        e_occ += e_occ
        e_virt += e_virt
    
    print "S =",i,"\t",len(e_all),"\t",len(e_occ),"\t",len(e_virt)

    if len(e_all) == 0:     # if the run fails to converge
        e_all = [10]*Nall
        e_occ = [10]*Nocc
        e_virt = [10]*(Nall-Nocc)

    mat_all[:,i] = e_all
    mat_occ[:,i] = e_occ

outfile_all = base_dir+outdir+"/evals_Pt"+cluster+".out"
outfile_occ = base_dir+outdir+"/evals_Pt"+cluster+"_occ.out"
savedata(mat_all,outfile_all)
savedata(mat_occ,outfile_occ)

