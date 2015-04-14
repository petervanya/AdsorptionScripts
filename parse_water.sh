#!/bin/bash

usage() {
  echo "Usage: $0
  Summarised table of of water on Pt adsorption runs
  for each position (top, bridge, fcc) and each spin

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

dir=~/Platinum/Water
cluster=Pt$cluster
cd $dir/$cluster

echo -e "Eta \t Spin \t Success? \t Reason for failure \t Steps \t Max steps \t E \t Runtime d:h:m:s"

for j in {1..3}; do
  for i in {0..10}; do
    filecheck="Eta_$j/S_$i/Pt.out"
    if [ ! -e $filecheck ]; then
      echo "$filecheck: file does not exist."
      continue
    fi
    if [ `cat $filecheck | wc -l` == "0" ]; then
      echo "$filecheck: empty file."
      continue
    fi

    cd Eta_$j/S_$i
    if [ `tail -n 1 Pt.out | awk '{print $1}'` == "Normal" ]; then 
      succ="Yes"
      reason="NA"
      E=`cat Pt.out | grep "cycles$" | tail -1 | awk '{print $5}'`
    else 
      succ="No"
      E="NA"
      str=`tail -n 4 Pt.out | head -n 1 | awk '{print $1}'`
      if [ $str == "Convergence" ]; then
        reason="Conv failure"
      elif [ $str == "Error" ]; then
        reason="Ran out of steps"
      else 
        reason="NA"
      fi

    fi

    steps=`cat Pt.out | grep "^ Step number" | tail -1 | awk '{print $3}'`
    maxsteps=`cat Pt.out | grep "^ Step number" | tail -1 | awk '{print $NF}'`
    runtime=`cat Pt.out | grep "^ Job cpu" | awk '{print $4":"$6":"$8":"$10}'`
    
    echo -e $j "\t" $i "\t" $succ "\t" $reason "\t" $steps "\t" $maxsteps "\t" $E "\t" $runtime
    cd ../..
  done
done

