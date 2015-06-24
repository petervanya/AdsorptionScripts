#!/usr/bin/env python
"""
Collection of often used functions for
-- input/output
-- rotating, translating and printing data

2nd version
pv278@cam.ac.uk, 17/06/15
"""
import numpy as np
from math import *


class Atoms:
    """class to produce and manipulate xyz coords with atom names"""
    def __init__(self, names, coords):
        self.names = names
        self.coords = np.array(coords)

    def __len__(self):
        """number of atoms"""
        return len(self.coords)

    def __repr__(self):
        """print xyz onto screen"""
        M, N = self.coords.shape
        line = ""
        for i in range(M):
            line += self.names[i] + "\t"
            for j in range(N):
                line += "%.6f" % self.coords[i, j] + "\t"
            line += "\n"
        return line.rstrip("\n")

    def save(self, filename):
        """save xyz coords into file"""
        f = open(filename, "w")
        M, N = self.coords.shape
        for i in range(M):
            line = str(self.names[i])+"\t"
            for j in range(N):
                line += "%.6f" % self.coords[i, j] + "\t"
            line += "\n"
            f.write(line)
        f.close()
        print "Coords saved to",filename

    def shift(self, s):
        assert len(s) == 3
        s = np.array(s)
        self.coords += s

    def rotate(self, theta=0, phi=0):
        N = len(self)
        Rtheta = np.array([[cos(theta),0,-sin(theta)],
                           [0,         1, 0         ],
                           [sin(theta),0, cos(theta)]])
        Rphi = np.array([[cos(phi),-sin(phi),0],
                         [sin(phi), cos(phi),0],
                         [0,        0,       1]])
 
        for i in range(N):
            self.coords[i, :] = np.dot(Rtheta, self.coords[i, :])
        for i in range(N):
            self.coords[i, :] = np.dot(Rphi, self.coords[i, :])


if __name__ == "__main__":
     print "Testing the Atoms class:"
     coords = np.array([1,0,0] + [0,1,0] + [0,0,1]).reshape((3, 3))
     atoms = Atoms(["Pt"]*3, coords)
     print atoms
     
     s = np.arange(3)
     print "Shifting atoms by", s
     atoms.shift(s)
     print atoms

     atoms.coords = coords
     theta, phi = 90, 90
     print "Rotating atoms by theta=%i, phi=%i:" % (theta, phi)
     atoms.rotate(radians(theta), radians(phi))
     print atoms
