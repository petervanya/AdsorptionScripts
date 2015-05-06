#!/usr/bin/env python
"""
Usage:
    gen_water [-t <t>] [-f <phi>] [-s <s>] [-p <p>]

Generate xyz water coordinates in xz plane with the possibility of rotation.

Options:
    -h, --help              Show this message and exit
    -s <s>,--shift <s>      Shift of O above Pt atom in "x y z"
    -p <p>,--posPt <p>      Position of O atom in Pt lattice vectors in "x y z"
    -f <phi>,--phi=<phi>    Rotation around z-axis (phi) in degrees (done before theta)
    -t <t>,--theta=<t>      Rotation around y-axis (theta) in degrees

pv278@cam.ac.uk, 20/02/15
"""
import numpy as np
from numpy.matlib import repmat
#import argparse
from docopt import docopt
from math import *

def savedata(coords,atom_names,filename):
    f = open(filename,"w")
    M,N = coords.shape
    for i in range(M):
        line = str(atom_names[i]) + "\t"
        for j in range(N):
            line += "%.6f" % coords[i,j] + "\t"
        line += "\n"
        f.write(line)
    f.close()
    print "Water coords printed into file",filename

def init_water():
    """Initialise water molecule"""
    alpha = radians(104.45)                   # angle between H atoms
    l_OH = 0.9584                             # bond length between O and H
    coords = np.zeros((3,3))
    coords[1,0] += l_OH*sin(alpha/2)
    coords[2,0] += -l_OH*sin(alpha/2)
    coords[1:3,2] += l_OH*cos(alpha/2)
    return coords

def translation(coords,shift):
    """shift H2O atoms"""
    return coords + repmat(shift,3,1)

def walk_Pt(coords,shift):
    """shift H2O atoms in Pt lattice vectors"""
    aPt = 2.775
    vPt = aPt*sqrt(3.0)/2
    hPt = aPt*sqrt(2.0/3)
    basis = np.array([[aPt, aPt/2,  aPt/2],
                      [0.0, vPt,    vPt/3],
                      [0.0, 0.0,    hPt  ]])
    return coords + np.dot(basis,shift)

def rotate_theta(coords,theta):
    Rtheta = np.array([[cos(theta),0,-sin(theta)],
                       [0,         1, 0         ],
                       [sin(theta),0, cos(theta)]])

    for i in range(3):
        coords[i,:] = np.dot(Rtheta,coords[i,:])
    return coords

def rotate_phi(coords,phi):
    Rphi = np.array([[cos(phi),-sin(phi),0],
                     [sin(phi), cos(phi),0],
                     [0,        0,       1]])
    for i in range(3):
        coords[i,:] = np.dot(Rphi,coords[i,:])
    return coords


if __name__ == "__main__":
    args = docopt(__doc__,version=1.0)
#    print args
    
    coords = init_water()

    if args["--phi"]:
        phi = float(args["--phi"])
        coords = rotate_phi(coords,phi)
        print "Rotated by phi =",degrees(phi)

    if args["--theta"]:
        theta = float(args["--theta"])
        coords = rotate_theta(coords,theta)
        print "Rotated by theta =",degrees(theta)

    if args["--posPt"]:
        vectPt = np.array(args["--posPt"].split()).astype(float)
        coords = walk_Pt(coords, vectPt)

    if args["--shift"]:
        shift = np.array(args["--shift"].split()).astype(float)
        coords = translation(coords, shift)
#    print "Total Pt shift:",dist
    
    filename = "water.xyz"
    names = ["O","H","H"]
    savedata(coords,names,filename)
    
