#!/usr/bin/python
import argparse
import numpy as np
import re

# ===== functions
def printdata(A,header=True):
    if header:
        print "Spin\tconv\tE\t\tcycles\terr\truntime"
        print "-"*8*7
    M,N = A.shape
    for i in range(M):
      line=""
      for j in range(N):
        line+= str(A[i][j]+"\t")
      print line

# ===== parsing arguments
help="Script to parse values from output files"
parser=argparse.ArgumentParser(description=help, epilog="pv278@cam.ac.uk, 28/04/15")

parser.add_argument("-d","--dir",dest="dirname",action="store",type=str,
                    metavar="d",help="Directory with output files. Default: Plain")
parser.add_argument("-c","--cluster",dest="cluster",action="store",type=int,required=True,
                    metavar="c",help="Pt cluster")
parser.add_argument("-s","--sort",dest="sort",action="store_true",
                    help="If array should be sorted by energy")
args = parser.parse_args()

if args.dirname:
    dir = "/home/pv278/Platinum/"+args.dirname
else:
    dir = "/home/pv278/Platinum/Plain"

# ===== main part
spin_list=range(11)
conv     = []
spins    = []
E        = []
Ncycles  = []
err      = []
runtime  = []

for i in spin_list:
    fname = dir+"/Pt"+str(args.cluster)+"/S_"+str(i)+"/Pt.out"
    outfile = open(fname).readlines()
    
    conv.append("Yes" if "Normal" in outfile[-1] else "No")

    temp = [l for l in outfile if "Charge" in l][0].split()[-1][-2:]
    spins.append( (int(temp)-1)/2 )
  
    E.append([l for l in outfile if "SCF Done" in l][-1].split()[4])
  
    Ncycles.append([l for l in outfile if "cycles" in l][-1].split()[-2])
  
    err.append([l for l in outfile if "Conv=" in l][-1].split("=")[-2].split()[0].replace("D","e"))
    
    temp = [l for l in outfile if " Job cpu" in l][-1].split()
    runtime.append(temp[3]+":"+temp[5]+":"+temp[7]+":"+temp[9])

conv      = np.array([conv]).T
spins     = np.array([spins]).T
E         = np.array([E]).T
Ncycles   = np.array([Ncycles]).T
err       = np.array([err]).T
runtime   = np.array([runtime]).T

A = np.concatenate((spins,conv,E,Ncycles,err,runtime),1)
if args.sort: 
    A = A[A[:,1].argsort()]
    A = A[::-1,:]

printdata(A)





