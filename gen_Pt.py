#!/usr/bin/python
"""
Script to create coordinates of atoms for certain Pt clusters
used by Goddard
12/2014
"""
import sys
import numpy as np
from math import sqrt


def printtofile(coords,filename):
    f=open(filename,"w")
    for i in range(coords.shape[0]):
      s=""
      for j in range(coords.shape[1]):
        s += "%.5f" % coords[i,j] + "\t"
      f.write( str("Pt\t")+s+"\n" )
    f.close()
    
# get the configuration into atoms
def get_config(config):
    arr = [int(i) for i in config.split("_")]
    num_atoms = sum(arr)
    return arr, num_atoms
    
def get_coords3(a,x0,y0,z0):
    v=sqrt(3.0)/2*a
    coords=np.zeros((3,3))
    coords[1,0] = a
    coords[2,0] = a/2
    coords[2,1] = v
    
    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords

def get_coords4(a,x0,y0,z0):
    v=sqrt(3.0)/2*a
    coords=np.zeros((4,3))
    for i in range(2):
      coords[1+i,0] = -a/2 + i*a
      coords[1+i,1] = v
    coords[3,1] = 2*v
    
    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
def get_coords6(a,x0,y0,z0):
    v=sqrt(3.0)/2*a
    coords=np.zeros((6,3))
    for i in range(3):
      coords[i,0] = i*a
    for i in range(2):
      coords[i+3,0] = a/2 + i*a
      coords[i+3,1] = v
    coords[5,0] = a
    coords[5,1] = 2*v
    
    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
def get_coords7(a,x0,y0,z0):
    v=sqrt(3.0)/2*a
    coords=np.zeros((7,3))
    for i in range(2):
      coords[i,0] = a/2 + i*a
    for i in range(3):
      coords[2+i,0] = i*a
      coords[2+i,1] = v
    for i in range(2):
      coords[5+i,0] = a/2 + i*a
      coords[5+i,1] = 2*v
    
    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
def get_coords8(a,x0,y0,z0):
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

    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
def get_coords12(a,x0,y0,z0):
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
    
    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
def get_coords10(a,x0,y0,z0):
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

    coords[:,0] += x0
    coords[:,1] += y0
    coords[:,2] += z0
    return coords
    
#######################################
a=2.775           # atom distance in A
v=sqrt(3.0)/2*a
h=sqrt(2.0/3.0)*a

config=sys.argv[1]
if len(sys.argv)>2:
  dir=str(sys.argv[2])
  print dir
else:
  dir=""
filename=str(dir+"Pt.xyz")
print "Coords saved in",filename

# ===== one layer
if config=="3":
  coords=get_coords3(a,0,0,0)

elif config=="4":
  coords=get_coords4(a,0,0,0)

elif config=="6":
  coords=get_coords6(a,0,0,0)

elif config=="7":
  coords=get_coords7(a,0,0,0)

elif config=="8":
  coords=get_coords8(a,0,0,0)

elif config=="10":
  coords=get_coords10(a,0,0,0)
   
elif config=="12":
  coords=get_coords12(a,0,0,0)

# ====== two layers
elif config=="6_3":
  arr,num_atoms=get_config(config)
  print "Total number of atoms: ",num_atoms
  coords=np.zeros((num_atoms,3))
  coords[:6,:] = get_coords6(a,0,0,0)
  coords[6:,:] = get_coords3(a,a/2,v/3,h)
   
elif config=="8_4":
   arr,num_atoms=get_config(config)
   print "Total number of atoms: ",num_atoms
   coords=np.zeros((num_atoms,3))
   coords[:8,:] = get_coords8(a,0,0,0)
   coords[8:,:] = get_coords4(a,a/2,v/3,h)
   
elif config=="12_7":
   arr,num_atoms = get_config(config)
   print "Total number of atoms: ",num_atoms
   coords=np.zeros((num_atoms,3))
   coords[:arr[0],:] = get_coords12(a,0,0,0)
   coords[arr[0]:,:] = get_coords7(a,a/2,v/3,h)

# ===== three layers
elif config=="5_10_5":
   arr,num_atoms = get_config(config)
   print "Total number of atoms: ",num_atoms
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
   coords[L1:L1+L2,:] = get_coords10(a,0,0,0)
   # 3rd layer
   for i in range(2):
     coords[L1+L2+i,0] = a/2 + a*i
     coords[L1+L2+i,1] = v/3
   for i in range(3):
     coords[L1+L2+i+2,0] = a*i
     coords[L1+L2+i+2,1] = 4*v/3
   for i in range(5):
     coords[L1+L2+i,2] = h
     
elif config=="9_10_9":
   arr,num_atoms = get_config(config)
   print "Total number of atoms: ",num_atoms
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
   coords[L1:L1+L2,:] = get_coords10(a,0,0,0)
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
   
else: 
  raise NotImplementedError

printtofile(coords,filename)

