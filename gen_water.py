#!/usr/bin/python
# =====
# 20/02/15
# Generate coords of water in xz plane
# 3 cmd ln args -- x,y,z shift from 0,0,0
# =====
import sys
import numpy as np
import numpy.matlib
import argparse
from math import pi, sqrt, sin, cos, radians, degrees

def printH2O(coordsH2O,filename):
		f=open(filename,"w")
		s = str("O\t")
		for j in range(3):
			s += "%.5f" % coordsH2O[0,j] + "\t"
		f.write(s+"\n")
		for i in range(1,3):
			s = str("H\t")
			for j in range(3):
				s += "%.5f" % coordsH2O[i,j] + "\t"
			f.write(s+"\n")
		f.close()

# ===== parse arguments
help_text = "Generate xyz water coordinates in yz plane."
sign_off = "Author: pv278@cam.ac.uk"
parser = argparse.ArgumentParser(description=help_text,epilog=sign_off)

parser.add_argument(
				"-pPt",
				"--posPt",
				dest="posPt",
				action="store",
				type=str,
				help="Position of O atom in Pt lattice vectors in the form 'a1_a2_a3'",
				metavar="p"
)

parser.add_argument(
				"-p",
				"--pos",
				dest="pos",
				action="store",
				type=str,
				help="Shift of O above Pt atom in the form 'x_y_z'",
				metavar="p"
)

parser.add_argument(
				"-phi",
				dest="angle_phi",
				action="store",
				type=float,
				default=0.0,
				help="Rotation around z-axis (phi) in degrees (done first)",
				metavar="t"
)

parser.add_argument(
				"-theta",
				dest="angle_theta",
				action="store",
				type=float,
				default=0.0,
				help="Rotation around y-axis (theta) in degrees",
				metavar="t"
)

arguments = parser.parse_args()

# ===== process input
dist=np.zeros(3)

if(arguments.pos):
	pos = arguments.pos.split("_")
	dist += [float(i) for i in pos]

aPt=2.775
vPt=aPt*sqrt(3.0)/2
hPt=aPt*sqrt(2.0/3)

basePt = np.array([[aPt, aPt/2,	aPt/2],
         	  	     [0.0, vPt,		vPt/3],
          	  	   [0.0, 0.0,		hPt  ]])

if(arguments.posPt):
	pos = arguments.posPt.split("_")
	pos = [float(i) for i in pos]
	dist += np.dot(basePt,np.array(pos))

print "Total shift: ", dist

# ===== water coords
alpha = radians(104.45)                   # angle between H atoms
l_OH = 0.9584                             # bond length between O and H
coords=np.zeros((3,3))
coords[1,1] += l_OH*sin(alpha/2)
coords[2,1] += -l_OH*sin(alpha/2)
coords[1:3,2] += l_OH*cos(alpha/2)

# ===== rotate and shift the molecule
phi = radians(arguments.angle_phi)
theta = radians(arguments.angle_theta)
Rphi = np.array([[cos(phi),-sin(phi),0],        # rotation matrix for phi
                 [sin(phi), cos(phi),0],
								 [0,        0,       1]])
Rtheta = np.array([[cos(theta),0,-sin(theta)],
                   [0,         1, 0         ],
									 [sin(theta),0, cos(theta)]])

for i in range(3):                        # rotation in phi
  coords[i,:] = np.dot(Rphi,coords[i,:])
print "Rotated by phi = ",degrees(phi)

for i in range(3):                        # rotation in theta
  coords[i,:] = np.dot(Rtheta,coords[i,:])
print "Rotated by theta = ",degrees(theta)

coords += np.matlib.repmat(dist,3,1)      # shift all atoms by dist

# ===== print into file
filename="water.xyz"
printH2O(coords,filename)
print "Water coords printed into file water.xyz"


