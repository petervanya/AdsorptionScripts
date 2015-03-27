#!/usr/bin/python
# =====
# script to generate oxygen coordinate
# 20/02/15
# =====
import sys
import numpy as np
import numpy.matlib
from math import pi, sqrt, sin, cos, radians

def savecoords(coords,filename):
		f=open(filename,"w")
		s = str("O\t")
		for j in range(3):
			s += "%.5f" % coords[0,j] + "\t"
		f.write(s+"\n")
		f.close()
		print "Coords saved in",filename

# ===== get input
dist=np.zeros((1,3))

if len(sys.argv)<4:
	print "You did not specify enough shift components, use default vector: [0,0,1] A."
	dist = np.array([[0,0,1]])
else:
	for i in range(3):
		dist[0,i] = float(sys.argv[i+1])

# ===== print into file
filename="O.xyz"
savecoords(dist,filename)
