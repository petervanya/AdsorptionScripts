#!/bin/bash

usage() {
  echo "Usage: $0
  Summarised table of each spin config for a Pt cluster from Gaussian outfiles
  Spin | converged? | Energy | Num cycles | Conv. error | Runtime

  Arguments:
  -h  show this message
  -c  Pt cluster, e.g. 9_10_9
  -d  Directory containing Pt*"
  exit 0
}

if [ $# -lt 1 ] ; then
  echo "You must specify at least one argument."
  usage
  exit 1
fi

while getopts ":hm:c:d:" opt; do
  case $opt in
   h) usage ;;
   c) cluster=$OPTARG ;;
   d) dir=$OPTARG
      echo $dir ;;
   :) echo "Missing argument -$OPTARG" >&2
      exit 1 ;;
  \?) echo "Invalid option: -$OPTARG" >&2
      exit 1 ;;
  esac
done
shift $((OPTIND - 1))

if [ -z $dir ]; then
  dir=~/Platinum/Plain
fi
cluster=Pt$cluster
cd $dir/$cluster

echo -e "Spin \t Conv? \t Energy \t Cycles \t Error \t Runtime d:h:m:s"

for i in {0..10}; do
  if [ `tail -n 1 S_$i/Pt.out | awk '{print $1}'` == "Normal" ]
    then conv="Yes"
    else conv="No"
  fi
  spin=`grep "^ Charge" S_$i/Pt.out | head -n 1 | awk '{print substr($NF,length($NF)-1,length($NF))}'`
  spin=`echo "($spin-1)/2" | bc`
  E_cycles=`cat S_$i/Pt.out | grep "cycles$" | awk '{print $5 "\t" $(NF-1)}'`
  err=`cat S_$i/Pt.out | grep "Conv=" | awk '{print substr($(NF-2),6,8)}'`
  runtime=`cat S_$i/Pt.out | grep "^ Job cpu" | awk '{print $4":"$6":"$8":"$10}'`

  echo -e $spin "\t" $conv "\t" $E_cycles "\t" $err "\t" $runtime
done

