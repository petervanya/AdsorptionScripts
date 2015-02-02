#!/usr/bin/python
# Script to generate Gaussian input file for 
# Pt clusters 9.10.9 with H20 on top
# 29/01/14
import sys
import numpy as np
from math import sqrt,sin,cos,radians


def printPt(coordsPt,filename):
    print coordsPt
    f=open(filename,"a")
    for i in range(coordsPt.shape[0]):
      s=""
      for j in range(3):
        s += "%.3f" % coordsPt[i,j] +"\t"
      s+="\tF"
      f.write( str("Pt ")+s+"\n" )
    f.write("\n")
    f.close()
    
def printH20(coordsH2O,filename):
		f=open(filename,"w")
		s = str("O ")
		for j in range(3):
			s += "%.3f" % coordsH2O[0,j] + "\t"
		f.write(s+"\n")
		for i in range(1,3):
			s = str("H ")
			for j in range(3):
				s += "%.3f" % coordsH2O[i,j] + "\t"
			f.write(s+"\n")
		f.close()

def freezeBonds(filename):
    f=open(filename,"a")
    f.write("1 2 0.958 F\n")
    f.write("1 3 0.958 F\n")
    f.close()
    
# get the configuration into atoms
def get_config(config):
    arr = [int(i) for i in config.split("_")]
    num_atoms = sum(arr)
    return arr, num_atoms
    
def get_coords10(a,x0,y0,z0):
		v=sqrt(3.0)/2*a
		coords=np.zeros((10,3))
		for i in range(3):
			coords[i,0] = a/2 + i*a
		for i in range(4):
			coords[i+3,0] = a*i
			coords[i+3,1] = v
		for i in range(3):
			coords[i+7,0] = a/2 + a*i
			coords[i+7,1] = 2*v

		coords[:,0] += x0
		coords[:,1] += y0
		coords[:,2] += z0
		return coords
		
def setH2Ocoords(Pt_atom_coords,dist):
		theta = radians(104.45)  # angle between H atoms
		l_OH = 0.9584            # bond length between O and H
		coords=np.zeros((3,3))
		for i in range(3):
			coords[i,:] = Pt_atom_coords + dist			# set O atom
		coords[1,0] += l_OH*sin(theta/2)          # shift x-coord of 1st H
		coords[2,0] += -l_OH*sin(theta/2)         # shift x-coord of 2nd H
		coords[1:3,2] += l_OH*cos(theta/2)        # shift z-coords of Hs
		print theta,cos(theta/2)
		return coords
    
# ===============================================
# main program
# ===============================================
a=2.775           # atom distance in A
v=sqrt(3.0)/2*a
h=sqrt(2.0/3.0)*a

filename=str("test.xyz")
config="9_10_9"
arr,num_atoms = get_config(config)
print "Total number of Pt atoms: ",num_atoms

L1=arr[0]
L2=arr[1]
L3=arr[2]
coords=np.zeros((num_atoms,3))
# 1st layer
for i in range(4):
	coords[i,0] = a*i
	coords[i,1] = 5*v/3
for i in range(3):
	coords[i+4,0] = a/2 + a*i
	coords[i+4,1] = 2*v/3
for i in range(2):
	coords[i+7,0] = a + a*i
	coords[i+7,1] = -v/3
# 2nd layer
coords[L1:L1+L2,:] = get_coords10(a,0,0,h)
# 3rd layer
for i in range(4):
	coords[L1+L2+i,0] = a*i
	coords[L1+L2+i,1] = v/3
for i in range(3):
	coords[L1+L2+i+4,0] = a/2 + a*i
	coords[L1+L2+i+4,1] = 4*v/3
for i in range(2):
	coords[L1+L2+i+7,0] = a + a*i
	coords[L1+L2+i+7,1] = 7*v/3
for i in range(9):   # shift vertically
	coords[L1+L2+i,2] = 2*h


# get H20 coords
dist = 3
dist_vect = np.array([0,0,3])
xyzH2O = np.array( setH2Ocoords(coords[24,:],dist_vect) )
print xyzH2O
	
# print into file
printH20(xyzH2O,filename)
printPt(coords,filename)
freezeBonds(filename)
