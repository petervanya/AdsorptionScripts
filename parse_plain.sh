#!/bin/bash
# =====
# Summarised table of each spin config for a Pt cluster from Gaussian outfiles
# Spin | converged? | N. cycles | Conv. error | Runtime
# Cmd ln args
# Cmd
# 1 -- cluster, e.g. 12_7
# =====

if [ "$1" == "-h" ]; then
  echo "Usage: "
fi

dir=~/Platinum/Plain
cluster=Pt$1
cd $dir/$cluster

echo -e "# Spin | Conv? | Energy | Cycles | Error | Runtime"

for i in {0..10}
do
  if [ `tail -n 1 S_$i/Pt.out | awk '{print $1}'` == "Normal" ]
  	then conv="Yes"
    else conv="No"
  fi
  cycles=`cat S_$i/Pt.out | grep "cycles$" | awk '{print $5 "\t" $(NF-1)}'`
  err=`cat S_$i/Pt.out | grep "Conv=" | awk '{print substr($(NF-2),6,8)}'`
  # printing time in minutes: $4=days, $6=hours, $8=minutes, $10=seconds
  #runtime=`cat S_$i/$cluster.out | grep "^ Job cpu" | awk '{printf "%.1f", ($4*24*60*60 + $6*60*60 + $8*60 + $10)/60}'`
  runtime=`cat S_$i/Pt.out | grep "^ Job cpu" | awk '{print $4":"$6":"$8":"$10}'`

  echo -e $i "\t" $conv "\t" $cycles "\t" $err "\t" $runtime
done  
