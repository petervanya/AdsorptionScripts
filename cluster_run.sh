#!/bin/bash

# USAGE
# =====
# -- 1st cmd line arg: dir name of medium, e.g. Oxygen, Water or Plain
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
# =======================

medium=$1          # e.g. Oxygen or Water
config=$2          # e.g. Pt9_10_9

cd /home/pv278/Adsorption/$medium/$config;
/home/Gaussian/g09/g09 < $config.gjf > $config.out
