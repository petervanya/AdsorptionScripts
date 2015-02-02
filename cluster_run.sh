#!/bin/bash

# USAGE
# =====
# -- 1st cmd line arg: basis set (LanL2MB or LanL2DZ)
# -- 2nd cmd line arg: configuration (e.g. 5_10_5)
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
.$g09root/g09/bsd/g09.profile
# =======================

config=$1                 # e.g. 9_10_9

for i in 6
do
  cd /home/pv278/Adsorption/Jobs/Pt$config/S_$i;
  /home/Gaussian/g09/g09 < adsorp.gjf > adsorp.out
  cd /
done
