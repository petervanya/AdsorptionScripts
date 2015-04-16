#!/usr/bin/python
"""
Script to rotate a molecule
16/04/15
"""
import sys
import argparse
import numpy as np
from numpy.linalg import norm
from numpy.matlib import repmat
from scipy.linalg import expm
from math import *

help_text="Script to centre, shift, align or rotate a molecule by a given angle."
parser = argparse.ArgumentParser(description=help_text)

parser.add_argument("-f","--file",dest="file",action="store",type=str,required=True,
                    help="Input file name",metavar="fname")

parser.add_argument("-c","--centre",dest="centre",action="store",type=int,
                    help="Atom number to center the molecule around",metavar="n")

parser.add_argument("-a","--align",dest="align",action="store",type=str,
                    help="Align s.t. two atoms n,m lie on x-axis",metavar="m_n")
                    
parser.add_argument("-r","--rotate",dest="rotate",action="store",type=str,
                    help="Rotate by angles theta and phi",metavar="t_p")
                    
parser.add_argument("-s","--shift",dest="shift",action="store",type=str,
                    help="Final shift of all atoms by a vector",metavar="a_b_c")
                    
args = parser.parse_args()

# ====== read the file
f=open(args.file)
A=f.read().split("\n")
B=[line.split("\t") for line in A]
B.pop(-1)
B=np.array(B)
C = B[:,1:4].astype(np.float)
N=C.shape[0]

#vec1=C[0,:]  # carbon
#vec2=C[4,:]  # sulfur
#dist12 = norm(vec1-vec2)

# ===== shift
if(args.centre):
  n = int(args.centre)
  if n not in range(1,N+1):
    raise ValueError
  else:
    shift_vec = C[n-1,:] #np.array([float(i) for i in args.shift("_")])
    C -= repmat(shift_vec,N,1)

# ===== align atoms n1 and n2 to -- SO(3) rotation
if(args.align):
	n1,n2 = [int(i) for i in args.align.split("_")]
	if (n1 not in range(1,N+1)) or (n2 not in range(1,N+1)):
	  raise ValueError
	vec12 = C[n1-1,:] - C[n2-1,:]
	axis = np.array([1,0,0])
	alpha = acos( np.dot(vec12,axis)/norm(vec12) )
	omega = np.cross(vec12,axis)
	omega /= norm(omega)
	R = np.matrix([[0,        -omega[2], omega[1]],
		             [ omega[2], 0,       -omega[0]],
		             [-omega[1], omega[0], 0       ]])
	R *= -alpha

	for i in range(N):
		C[i,:] = np.dot(C[i,:],expm(R))
	#print C

# ===== rotate by given theta and phi
if(args.rotate):
	theta,phi = [radians(float(i)) for i in args.rotate.split("_")]
	Rphi = np.array([[cos(phi),-sin(phi),0],
		               [sin(phi), cos(phi),0],
		               [0,        0,       1]])
	#print Rphi
	Rtheta = np.array([[cos(theta),0,-sin(theta)],
		                 [0,         1, 0         ],
		                 [sin(theta),0, cos(theta)]])
	#print Rtheta

	for i in range(N):                        # rotation in phi
		C[i,:] = np.dot(Rphi,C[i,:])
	print "Rotated by phi =",degrees(phi)

	for i in range(N):                        # rotation in theta
		C[i,:] = np.dot(Rtheta,C[i,:])
	print "Rotated by theta =",degrees(theta)

# ===== final shift
if(args.shift):
  S = repmat([float(i) for i in args.shift.split("_")],N,1)
  C += S

B[:,1:4] = C
f=open("out.xyz","w")
for i in range(N):
  str=B[i,0] + "\t%.6f"%C[i,0] + "\t%.6f"%C[i,1] + "\t%.6f"%C[i,2] + "\n"
  f.write(str)
f.close()



