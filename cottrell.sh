#!/bin/bash

# USAGE
# =====
# -- 1st cmd ln arg: dir name "Water" or "Plain"
# -- 2nd cmd ln arg: file name without extension
# =====

# Generic Cottrell header
# =======================
#$ -cwd                                                                         
#$ -j y                                                                         
#$ -S /bin/bash                                                                 

# Gaussian commands                                                             
g09root="/home/Gaussian"
GAUSS_SCRDIR="/state/partition1/Gaussian_scratch"
GAUSS_EXEDIR="/home/Gaussian/g09/bsd:/home/Gaussian/g09/private:/home/Gaussian/g09"
export g09root GAUSS_SCRDIR GAUSS_EXEDIR
. $g09root/g09/bsd/g09.profile
# =======================

dir=$1                    # "Water" or "Plain"
config=$2                 # e.g. Pt9_10_9/Eta_*/S_*

cd /home/pv278/Platinum/$dir/$config
/home/Gaussian/g09/g09 < Pt.gjf > Pt.out
