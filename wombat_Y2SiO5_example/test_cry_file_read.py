""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,

- AlignToRefs which calculates a UB matrix based on supplied Qx, Qy, Qz and corresponding h,k,l

- 3Dalign which lets you specify projection vectors in h,k,l (r.l.u.) for the 3D viewer 

- Viewer3D 
    - this script demonstrates Viewer3D for datasets containing multiple HDF files
      (the idea being you can stitch together many HDF to cover all of reciprocal space)
    - shows reciprocal space in r.l.u. given the UB matrix and projection vectors

Test data: Y2SiO5 dataset
"""
import sys
# add location of Wombat DMCpy scripts
sys.path.append('J:\wombat_instrument_work\DMCpy_for_wombat\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
from wombatDMCpy._tools import readCryFileFromInt3D
import numpy as np
import matplotlib.pyplot as plt


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ get the data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# sample name (just used when saving figs)
sample_name = 'Y2SiO5'
# directory where the data are
data_dir = os.getcwd() + '/Y2SiO5_data/'
# currently all HDF must be of the same dimension
# here 676 and 677 both have 600 steps but 678 has 601 steps so we leave it out
file_name_list = ['WBT0102676.nx.hdf', 'WBT0102677.nx.hdf']
# Rotation axis in this case was Euler Phi
sample_rotation_axis = 'ephi'


unit_cell, int3D_UB_matrix = readCryFileFromInt3D('UB1.cry')

# For plotting in r.l.u. you need to supply a unit cell
# here we use the C2/c unit cell for Y2SiO5
# format is [a, b, c, alpha, beta, gamma]
unit_cell = np.array([14.406, 6.728, 10.421, 90, 122.194, 90]) 

# View 3D axis options, select one
axis_option = 2 # view scattering plane defined by projection vectors
#axis_option = 1 # view out-of-plane (orthogonal plane #1 to the plane defined by projection vectors)
#axis_option = 0 # view other out-of-plane (orthogonal plane #2 to the plane defined by projection vectors)

# Load the data
data_file_list = []
for i in range(len(file_name_list)):
    file_name = file_name_list[i]
    file_path = data_dir + file_name
    df = WombatDataFile.loadWombatDataFile(file_path,
                                           #twoThetaPosition=twoThetaOffset, 
                                           fileType = 'singlecrystal',
                                           unitCell = unit_cell, # associate the unit cell with the data
                                           wavelength=2.41, # Wavelength in angstroms
                                           radius=0.728, # Wombat sample-detector distance
                                           sampleRotationAxis = sample_rotation_axis)
    data_file_list.append(df)

# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

"""~~~~~~ UB Matrix and aligning data to projection vectors in r.l.u. ~~~~~~~"""
######## Use UB matrix from Int3D (RECOMMENDED)
int3D_UB_matrix = np.array([[-0.07128796726465, -0.00493851210922, -0.00514440611005],
                            [0.04053531959653, -0.00255302991718,  0.11326986551285],
                            [-0.00167354044970,  0.14852857589722,  0.00177592528053]])
chi_angle_deg = 0.00 # if omega scan data acquired with nonzero ephi and echi
phi_angle_deg = 0.00
ds.useUBmatrixFromInt3D(int3D_UB_matrix, echi = chi_angle_deg, ephi = phi_angle_deg)
