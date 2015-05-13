#!/usr/bin/env python
"""Usage:
    parse (plain | water) <cluster> [-d <d>] [-s] (--print | --save)

Script to parse values from output files

Arguments:
    <cluster>         Pt cluster, e.g. 9_10_9

Options:
    -h,--help         Show this message and exit
    -d <d>,--dir=<d>  Dir w output files after ~/Platinum/ [Default: Plain]
    -s,--sort         Sort the spin states by energy

pv278@cam.ac.uk, 28/04/15
"""
from docopt import docopt
import numpy as np
from iolib import save_table

def print_table(A,header):
    if header:
        print header
    M,N = A.shape
    for i in range(M):
        line=""
        for j in range(N):
            line += str(A[i][j]) + "\t"
        print line

def get_path(Pt_dir,spin,eta=0):
    """get full file path with eta and spin"""
    if eta != 0:
        path = Pt_dir + "Water" + "/Pt" + str(cluster) + "/Eta_" + str(eta) + "/S_" + str(spin) + "/Pt.out"
    else:
        path = Pt_dir + "Plain" + "/Pt" + str(cluster) + "/S_" + str(spin) + "/Pt.out"
    return path

def get_table_plain(Pt_dir,spin_list):
    """get table of all data for all spins"""
    conv     = []
    spins    = []
    E        = []
    Ncycles  = []
    err      = []
    runtime  = []

    for i in spin_list:
        outfile = open(get_path(Pt_dir,i)).readlines()
        
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
    return A

def get_table_water(Pt_dir,spin_list):
    """get table of all data for water runs"""
    spins    = []
    succ     = []
    reason   = []
    E        = []
    steps    = []
    maxsteps = []
    runtime  = []
    datetime = []
    
    for j in range(1,4):
        for i in spin_list:
            outfile = open(get_path(Pt_dir,i,j)).readlines()
        
            temp = [l for l in outfile if "Charge" in l][0].split()[-1][-2:]
            spins.append( (int(temp)-1)/2 )
            
            if "Normal" in outfile[-1]:
                succ.append("Yes")
                reason.append("NA")
                E.append([l for l in outfile if "SCF Done" in l][-1].split()[4])
            else:
                succ.append("No")
                E.append("NA")
                err_word = outfile[-4].split()[0]
                if err_word == "Convergence":
                    reason.append("Conv fail")
                elif err_word == "Error":
                    reason.append("Out of steps")
                else:
                    reason.append("Unknown")

            temp = [l for l in outfile if "Step number" in l]
            if len(temp) == 0:
                steps.append(0)
                maxsteps.append(0)
            else:
                steps.append(temp[-1].split()[2])
                maxsteps.append(temp[-1].split()[-1])
            temp = [l for l in outfile if " Job cpu" in l][-1].split()
            runtime.append(temp[3]+":"+temp[5]+":"+temp[7]+":"+temp[9])
            
            temp = [l for l in outfile if "termination" in l][-1].split()
            datetime.append(temp[-4]+" "+temp[-3]+" "+temp[-1]+" "+temp[-2])
    
    etas      = np.array([[1]*11 + [2]*11 + [3]*11]).T
    spins     = np.array([spins]).T
    succ      = np.array([succ]).T
    reason    = np.array([reason]).T
    steps     = np.array([steps]).T
    maxsteps  = np.array([maxsteps]).T
    E         = np.array([E]).T
    runtime   = np.array([runtime]).T
    datetime  = np.array([datetime]).T
 
    A = np.concatenate((etas,spins,succ,reason,steps,maxsteps,E,runtime,datetime),1)
    return A

if __name__ == "__main__":
    args = docopt(__doc__,version=0.1)
#    print args
    
    cluster = int(args["<cluster>"])
    Pt_dir = "/home/pv278/Platinum/"
    spin_list=range(11)

    if args["plain"]:
        A = get_table_plain(Pt_dir, spin_list)
        header = "Spin\tconv\tE\t\tcycles\terr\truntime"
        outfile_path = Pt_dir + "Plain" + "/Outfiles/"
        
    elif args["water"]:
        A = get_table_water(Pt_dir, spin_list)
        header = "Eta\tSpin\tSucc\tReason\tSteps\tMSteps\tE\truntime\tDate"
        outfile_path = Pt_dir + "Water" + "/Outfiles/"
    
    if args["--sort"]:
        A = A[A[:,1].argsort()]
        A = A[::-1,:]
    
    if args["--print"]:
        print_table(A,header)

    if args["--save"]:
        filename = "Pt" + str(cluster) + "_summary.out"
        save_table(A,outfile_path + filename)



