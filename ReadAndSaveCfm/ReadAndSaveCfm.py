'''
This script reads in the tsurf (*.ts) files for the SCEC Community Fault Model (cfm)
as a numpy array.

The script is based on the matlab script ReadAndSaveCfm.m by Brendan Meade available
from http://structure.rc.fas.harvard.edu/cfm/download/meade/ReadAndSaveCfm.m

Copyright Paul Kaeufl, July 2014
'''
import numpy as np
import glob
import sys

def readTsCoords(filename):
    f = file(filename, 'r')
    lines = f.readlines()
    f.close()
    idxVrtx = [idx for idx,l in enumerate(lines) 
               if 'VRTX' in l or 'PVRTX' in l]
    idxTrgl = [idx for idx,l in enumerate(lines) if 'TRGL' in l]
    nVrtx = len(idxVrtx)
    nTrgl = len(idxTrgl)
    vrtx = np.zeros((nVrtx, 4))
    trgl = np.zeros((nTrgl, 3), dtype='int')
    tri = np.zeros((nTrgl, 3, 3))
    for k, iVrtx in enumerate(idxVrtx):
        line = lines[iVrtx]
        tmp = line.split(' ')
        vrtx[k] = [int(tmp[1]), float(tmp[2]), float(tmp[3]), float(tmp[4])]
    
    for k, iTrgl in enumerate(idxTrgl):
        line = lines[iTrgl]
        tmp = line.split(' ')
        trgl[k] = [int(tmp[1]), int(tmp[2]), int(tmp[3])]
        for l in range(3):
            for m in range(3):
                tri[k,l,m] = vrtx[vrtx[:,0]==trgl[k, m]][0, l+1]
    return vrtx, trgl, tri
    
if __name__ == '__main__':
    if len(sys.argv)>1:
        path = sys.argv[1]
    else:
        path = '.'
    output_file = path+'/cfm.npy'
    filenames = glob.glob(path+'/*.ts')
    goodFiles = []
    badFiles = []
    cfm = {}
    for filename in filenames:
        print "Working on %s" % filename
        try:
            vrtx,trgl,tri = readTsCoords(filename)
            name = filename.split('/')[-1][:-3]
            cfm[name] = {}
            cfm[name]['vrtx'] = vrtx
            cfm[name]['trgl'] = trgl
            cfm[name]['tri'] = tri
            goodFiles.append(filename)
        except:
            print "Failed to read %s" % filename
            badFiles.append(filename)
    print "Tried %i files. Found %i good and %i bad." % (len(filenames), len(goodFiles), len(badFiles))
    np.save(output_file, cfm)