#!/bin/bash
# =====
# Summarising output of each spin config for a Pt cluster 
# from Gaussian outfiles
# Spin | converged? | N. cycles | Conv. error | Runtime
# 1st cmd ln arg -- cluster, e.g. 12_7
# =====

dir=~/Adsorption/Plain
cluster=Pt$1
cd $dir/$cluster

#echo -e "# Spin \t Conv \t Num. cycles \t Err \t Runtime"

for i in {0..10}
do
  if [ `tail -n 1 S_$i/$cluster.out | awk '{print $1}'` == "Normal" ]; then
    conv="Yes"
  else
    conv="No"
  fi
  cycles=`cat S_$i/$cluster.out | grep "cycles$" | awk '{print $5 "\t" $(NF-1)}'`
  err=`cat S_$i/$cluster.out | grep "Conv=" | awk '{print substr($(NF-2),6,8)}'`
  # printing time: $4=days, $6=hours, $8=minutes, $10=seconds
  runtime=`cat S_$i/$cluster.out` | grep "^ Job cpu" | awk '{print ($4*24*60*60 + $6*60*60 + $8*60 + $10)/60}'`

	echo -e $i "\t" $conv "\t" $cycles "\t" $err "\t" $runtime
done  
