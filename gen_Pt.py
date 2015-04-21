#!/usr/bin/python
"""
Script to create coordinates of atoms for certain Pt clusters
used by Jacob et al.
Created: 12/2014
"""
import sys
import argparse
import numpy as np
from numpy.matlib import repmat
from math import sqrt

help="Generate coordinates of small Pt clusters according to Jacob et al."
parser=argparse.ArgumentParser(description=help,epilog="Author: pv278@cam.ac.uk")

parser.add_argument("-c","--cluster",dest="cluster",action="store",type=str,required=True,
                    metavar="c",help="Cluster type, e.g. 9_10_9")
                    
parser.add_argument("-s","--shift",dest="shift",action="store",type=str,
                    metavar="s",help="Shift the initial atom by a vector x_y_z")
                                        
parser.add_argument("-dir","--dir",dest="dir",action="store",type=str,
                    metavar="dir",help="Directory to save the produced file")
                    
args=parser.parse_args()

def printtofile(coords,filename):
    f=open(filename,"w")
    for i in range(coords.shape[0]):
      s=""
      for j in range(coords.shape[1]):
        s += "%.5f" % coords[i,j] + "\t"
      f.write( str("Pt\t")+s+"\n" )
    f.close()
    
# get the cluster type from the string input
def get_cluster(cluster):
    arr = [int(i) for i in cluster.split("_")]
    num_atoms = sum(arr)
    return arr, num_atoms
    
def get_coords3(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((3,3))
    coords[1,0] = a
    coords[2,0] = a/2
    coords[2,1] = v
    
    coords += shift
    return coords

def get_coords4(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((4,3))
    for i in range(2):
      coords[1+i,0] = -a/2 + i*a
      coords[1+i,1] = v
    coords[3,1] = 2*v
    
    coords += shift
    return coords
    
def get_coords6(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((6,3))
    for i in range(3):
      coords[i,0] = i*a
    for i in range(2):
      coords[i+3,0] = a/2 + i*a
      coords[i+3,1] = v
    coords[5,0] = a
    coords[5,1] = 2*v
    
    coords += shift
    return coords
    
def get_coords7(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((7,3))
    for i in range(2):
      coords[i,0] = i*a
    for i in range(3):
      coords[2+i,0] = -a/2 + i*a
      coords[2+i,1] = v
    for i in range(2):
      coords[5+i,0] = i*a
      coords[5+i,1] = 2*v
    
    coords += shift
    return coords
    
def get_coords8(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((8,3))
    coords[1,0] = a
    for i in range(3):
      coords[2+i,0] = -a/2 + i*a
      coords[2+i,1] = v
    for i in range(2):
      coords[5+i,0] = i*a
      coords[5+i,1] = 2*v
    coords[7,0] = a/2
    coords[7,1] = 3*v

    coords += shift
    return coords
    
def get_coords12(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((12,3))
    for i in range(3):
      coords[i,0] = i*a
    for i in range(4):
      coords[3+i,0] = -a/2 + i*a
      coords[3+i,1] = v
    for i in range(3):
      coords[7+i,0] = i*a
      coords[7+i,1] = 2*v
    for i in range(2):
      coords[10+i,0] = a/2 + i*a
      coords[10+i,1] = 3*v
    
    coords += shift
    return coords
    
def get_coords10(a,shift=[0,0,0]):
    v=sqrt(3.0)/2*a
    coords=np.zeros((10,3))
    for i in range(3):
      coords[i,0] = a*i
    for i in range(4):
      coords[i+3,0] = -a/2 + a*i
      coords[i+3,1] = v
    for i in range(3):
      coords[i+7,0] = a*i
      coords[i+7,1] = 2*v

    coords += shift
    return coords
    
# ===== Main part
a=2.775                    # atom distance in Angstroms
v=sqrt(3.0)/2*a
h=sqrt(2.0/3.0)*a
cluster=args.cluster
if args.shift:
  shift=np.array([float(i) for i in args.shift.split("_")])
  print "Shift =",shift
else:
  shift=[0,0,0]

if args.dir:
  dir=args.dir
  print dir
else:
  dir=""
filename=str(dir+"Pt.xyz")

# ===== one layer
if cluster=="3":
  coords=get_coords3(a,shift=[0,0,0])

elif cluster=="4":
  coords=get_coords4(a,shift=[0,0,0])

elif cluster=="6":
  coords=get_coords6(a,shift=[0,0,0])

elif cluster=="7":
  coords=get_coords7(a,shift=[0,0,0])

elif cluster=="8":
  coords=get_coords8(a,shift=[0,0,0])

elif cluster=="10":
  coords=get_coords10(a,shift=[0,0,0])
   
elif cluster=="12":
  coords=get_coords12(a,shift=[0,0,0])

# ====== two layers
elif cluster=="6_3":
  arr,num_atoms=get_cluster(cluster)
  coords=np.zeros((num_atoms,3))
  coords[:6,:] = get_coords6(a,[0,0,0])
  coords[6:,:] = get_coords3(a,[a/2,v/3,h])
  coords += repmat(shift,num_atoms,1)
   
elif cluster=="8_4":
   arr,num_atoms=get_cluster(cluster)
   coords=np.zeros((num_atoms,3))
   coords[:8,:] = get_coords8(a)
   coords[8:,:] = get_coords4(a,[a/2,v/3,h])
   coords += repmat(shift,num_atoms,1)
   
elif cluster=="12_7":
   arr,num_atoms = get_cluster(cluster)
   coords=np.zeros((num_atoms,3))
   coords[:arr[0],:] = get_coords12(a)
   coords[arr[0]:,:] = get_coords7(a,[a/2,v/3,h])
   coords += repmat(shift,num_atoms,1)

# ===== three layers
elif cluster=="5_10_5":
   arr,num_atoms = get_cluster(cluster)
   L1=arr[0]
   L2=arr[1]
   L3=arr[2]
   coords=np.zeros((num_atoms,3))
   # 1st layer
   for i in range(3):
     coords[i,0] = a*i
     coords[i,1] = 2*v/3
   for i in range(2):
     coords[i+3,0] = a/2 + a*i
     coords[i+3,1] = 5*v/3
   for i in range(5):
     coords[i,2] = -h
   # 2nd layer
   coords[L1:L1+L2,:] = get_coords10(a)
   # 3rd layer
   for i in range(2):
     coords[L1+L2+i,0] = a/2 + a*i
     coords[L1+L2+i,1] = v/3
   for i in range(3):
     coords[L1+L2+i+2,0] = a*i
     coords[L1+L2+i+2,1] = 4*v/3
   for i in range(5):
     coords[L1+L2+i,2] = h
   coords += repmat(shift,num_atoms,1)
     
elif cluster=="9_10_9":
   arr,num_atoms = get_cluster(cluster)
   L1=arr[0]
   L2=arr[1]
   L3=arr[2]
   coords=np.zeros((num_atoms,3))
   # 1st layer
   for i in range(4):
     coords[i,0] = -a/2 + a*i
     coords[i,1] = -v/3
   for i in range(3):
     coords[i+4,0] = a*i
     coords[i+4,1] = -v/3 + v
   for i in range(2):
     coords[i+7,0] = a/2 + a*i
     coords[i+7,1] = -v/3 + 2*v
   for i in range(L1):
     coords[i,2] = -h
   # 2nd layer
   coords[L1:L1+L2,:] = get_coords10(a)
   # 3rd layer
   for i in range(2):
     coords[L1+L2+i,0] = a/2 + a*i
     coords[L1+L2+i,1] = v/3
   for i in range(3):
     coords[L1+L2+i+2,0] = a*i
     coords[L1+L2+i+2,1] = v/3 + v
   for i in range(4):
     coords[L1+L2+i+5,0] = -a/2 + a*i
     coords[L1+L2+i+5,1] = v/3 + 2*v
   for i in range(L3):
     coords[L1+L2+i,2] = h
   coords += repmat(shift,num_atoms,1)
   
else:
  print "Cluster not implemented, please choose a different one."
  raise SystemExit #raise NotImplementedError

# ===== print to file
printtofile(coords,filename)
print "Coords of cluster",args.cluster,"saved in",filename

