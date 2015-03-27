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
from math import pi, sqrt, sin, cos, radians

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
help_text = "Generate xyz water coordinates in vertical plane"
sign_off = "Author: pv278@cam.ac.uk"
parser = argparse.ArgumentParser(description=help_text,epilog=sign_off)
parser.add_argument(
				"-e",
				"--eta",
				dest="eta",
				action="store",
				type=int,
				help="Position on surface: 0=custom, 1=top, 2=bridge, 3=fcc",
				metavar="n"
)

parser.add_argument(
				"-p",
				"--pos",
				dest="pos",
				action="store",
				type=str,
				help="Coordinates in the form 'x_y_z'",
				metavar="x_y_z"
)

parser.add_argument(
				"-pPt",
				"--posPt",
				dest="posPt",
				action="store",
				type=str,
				help="Coordinates in Pt lattice vectors in the form 'x_y_z'",
				metavar="x_y_z"
)

arguments = parser.parse_args()

# ===== process input
dist=np.zeros(3)
#if len(sys.argv)<4:
#	print "You did not specify enough shift components, use default vector: [0,0,1] A."
#	dist = [0,0,1]
#else:
#	for i in range(3):
#		dist[i] = float(sys.argv[i+1])
#	print "Shift distance: ",dist

eta = arguments.eta

if(arguments.pos):
	pos = arguments.pos.split("_")
	dist = [float(i) for i in pos]
	print "Shift distance: ", dist

aPt=2.775
vPt=aPt*sqrt(3.0)/2
hPt=aPt*sqrt(2.0/3)

basePt = np.array([[aPt,	aPt/2,aPt/2],
         	  	     [0.0, vPt,		vPt/3],
          	  	   [0.0, 0.0,		hPt]])

if(arguments.posPt):
	pos = arguments.posPt.split("_")
	dist = [float(i) for i in pos]
	dist = np.dot(basePt,np.array(dist))
	print "Shift distance: ", dist

# ===== water coords
theta = radians(104.45)                   # angle between H atoms
l_OH = 0.9584                             # bond length between O and H
coords=np.zeros((3,3))
coords[1,1] += l_OH*sin(theta/2)          # shift x-coord of 1st H
coords[2,1] += -l_OH*sin(theta/2)         # shift x-coord of 2nd H
coords[1:3,2] += l_OH*cos(theta/2)        # shift z-coords of Hs

coords += np.matlib.repmat(dist,3,1)      # shift all atoms by dist

# ===== print into file
filename="water.xyz"
printH2O(coords,filename)
print "Water coords printed into file water.xyz"


