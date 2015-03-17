#!/bin/bash
# =====
# Summarising output for each Pt cluster and each spin config
# spin | converged? | cycles
# 1st cmd ln arg -- cluster, e.g. 12_7
# =====

dir=../Plain
cluster=Pt$1
cd $cluster

#echo -e "# Spin \t Conv \t Num. cycles \t Err \t Runtime"

for i in {0..10}
do
  if [ `tail -n 1 $dir/S_$i/$cluster.out | awk '{print $1}'` == "Normal" ]; then
    conv="Yes"
  else
    conv="No"
  fi
  cycles=`cat $dir/S_$i/$cluster.out | grep "cycles$" | awk '{print $5 "\t" $(NF-1)}'`
  err=`cat $dir/S_$i/$cluster.out | grep "Conv=" | awk '{print substr($(NF-2),6,8)}'`
  # printing time: $4=days, $6=hours, $8=minutes, $10=seconds
  runtime=`grep "^ Job cpu" $dir/S_$i/$cluster.out | awk '{print ($4*24*60*60 + $6*60*60 + $8*60 + $10)/60}'`

	echo -e $i "\t" $conv "\t" $cycles "\t" $err "\t" $runtime
done  
