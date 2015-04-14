#!/bin/bash

usage() {
  echo "Usage: $0
  Summarised table of each spin config for a Pt cluster from Gaussian outfiles
  Spin | converged? | Energy | Num cycles | Conv. error | Runtime

  Arguments:
  -h  show this message
  -c  Pt cluster, e.g. 9_10_9"
  exit 0
}

if [ $# -lt 1 ] ; then
  echo "You must specify at least one argument."
  usage
  exit 1
fi

while getopts ":hm:c:" opt; do
  case $opt in
   h) usage ;;
   c) cluster=$OPTARG ;;
   :) echo "Missing argument -$OPTARG" >&2
      exit 1 ;;
  \?) echo "Invalid option: -$OPTARG" >&2
      exit 1 ;;
  esac
done
shift $((OPTIND - 1))

dir=~/Platinum/Plain
cluster=Pt$cluster
cd $dir/$cluster

echo -e "# Spin | Conv? | Energy | Cycles | Error | Runtime d:h:m:s"

for i in {0..10}; do
  if [ `tail -n 1 S_$i/Pt.out | awk '{print $1}'` == "Normal" ]
    then conv="Yes"
    else conv="No"
  fi
  E_cycles=`cat S_$i/Pt.out | grep "cycles$" | awk '{print $5 "\t" $(NF-1)}'`
  err=`cat S_$i/Pt.out | grep "Conv=" | awk '{print substr($(NF-2),6,8)}'`
  #
  # printing time in minutes: $4=days, $6=hours, $8=minutes, $10=seconds
  #runtime=`cat S_$i/$cluster.out | grep "^ Job cpu" | awk '{printf "%.1f", ($4*24*60*60 + $6*60*60 + $8*60 + $10)/60}'`
  #
  runtime=`cat S_$i/Pt.out | grep "^ Job cpu" | awk '{print $4":"$6":"$8":"$10}'`

  echo -e $i "\t" $conv "\t" $E_cycles "\t" $err "\t" $runtime
done

