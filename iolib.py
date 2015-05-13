#!/usr/bin/env python
"""
Collection of often used functions for
-- input/output
-- rotating, translating and printing data

pv278@cam.ac.uk, 11/05/15
"""
import numpy as np

def save_xyz(coords,atom_names,filename):
    """save xyz coords into file"""
    f = open(filename,"w")
    M,N = coords.shape
    for i in range(M):
        line = str(atom_names[i])+"\t"
        for j in range(N):
            line += "%.6f" % coords[i,j] + "\t"
        line += "\n"
        f.write(line)
    f.close()
    print "Coords saved to",filename


def save_table(A, filepath, header=False):
    """save table A into file"""
    f = open(filepath,"w")
    M,N = A.shape
    if header:
        f.write(header)
    for i in range(M):
        line = ""
        for j in range(N):
            line += str(A[i,j]) + "\t"
        line += "\n"
        f.write(line)
    f.close()
    print "Table saved to",filepath

def print_table(A,header=""):
    if header:
        print header
    M,N = A.shape
    for i in range(M):
        line=""
        for j in range(N):
            line += str(A[i][j]) + "\t"
        print line

def get_path(Pt_dir, cluster, spin, eta=0):
    """get full file path with eta and spin"""
    if eta != 0:
        path = Pt_dir + "Water" + "/Pt" + str(cluster) + "/Eta_" + str(eta) + "/S_" + str(spin) + "/Pt.out"
    else:
        path = Pt_dir + "Plain" + "/Pt" + str(cluster) + "/S_" + str(spin) + "/Pt.out"
    return path

def shift(coords,s):
    """shift coordinates by a given vector s"""
    return coords + repmat(s,3,1)

def rotate_theta(coords,theta):
    """rotate atoms by an angle theta (in radians)"""
    N = coords.shape[0]
    Rtheta = np.array([[cos(theta),0,-sin(theta)],
                       [0,         1, 0         ],
                       [sin(theta),0, cos(theta)]])

    for i in range(N):
        coords[i,:] = np.dot(Rtheta,coords[i,:])
    return coords

def rotate_phi(coords,phi):
    """rotate atoms by angle phi (in radians)"""
    N = coords.shape[0]
    Rphi = np.array([[cos(phi),-sin(phi),0],
                     [sin(phi), cos(phi),0],
                     [0,        0,       1]])
    for i in range(N):
        coords[i,:] = np.dot(Rphi,coords[i,:])
    return coords


def get_bandgap(cluster, spin, dir="/home/pv278/Platinum/"):
    """Extract band gap (highest occ value - lowest virt value)
       and from the files for a specific spin"""
    outfile = open(get_path(dir, cluster, spin)).readlines()
    line = [l for l in outfile if "occ" in l]
    if line:
        Eocc = line[-1].split()[-1]
    else:
        Eocc = None
    line = [l for l in outfile if "virt" in l]
    if line:
        Evirt = line[0].split()[4]
    else:
        Evirt = None
    
    if Eocc:
        return (float(Evirt) - float(Eocc))*27.211
    else:
        return

def get_all_bandgaps(cluster, spin_list, dir="/home/pv278/Platinum/"):
    """Extract band gaps for all spins"""
    E = []
    s = []
    for spin in spin_list:
        Ebg = get_bandgap(cluster, spin, dir)
        if Ebg:
            E.append(Ebg)
            s.append(spin)

    A = np.vstack((s,E))
    return A.T






