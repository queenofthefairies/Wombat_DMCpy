""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,

- AlignToRefs which calculates a UB matrix based on supplied Qx, Qy, Qz and corresponding h,k,l

- UB matrix properties

- calculateHKLtoA3A4Z which takes a given reflection hkl and then calculates "observables" 
    - A3 = sample rotation angle (degrees)
    - A4 = two theta (degrees)
    - z = vertical position from the middle of the detector (m)
    [A3, A4 and z are the co-ordinates defined in the original DMCpy package so
    we continue using this nomenclature.]

Test data: Y2SiO5 dataset
"""
import sys
# add location of Wombat DMCpy scripts
sys.path.append('J:\wombat_instrument_work\eulerian_cradle\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math



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
# For plotting in r.l.u. you need to supply a unit cell
# here we use the C2/c unit cell for Y2SiO5
# format is [a, b, c, alpha, beta, gamma]
unit_cell = np.array([14.406, 6.728, 10.421, 90, 122.194, 90]) 


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



"""~~~~~~ UB Matrix and aligning data to projection vectors in r.l.u. ~~~~~~~"""
# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

# Before you get to this bit, you need to index two peaks by hand 
# 1. use the reciprocal space viewer (Qx, Qy, Qz in inv Angstroms) in the 
#    other script Reciprocal_Space_View_invAA_Y2SiO5.py
# 2. choose a couple of peaks with Qz small and note their coordinates
# 3. use the reciprocal space conversion spreadsheet to figure out d spacing
#    and hopefully the d spacings/ 2theta line up with allowed peaks!
# 4. then come back here with your Qx, Qy, Qz and corresponding hypothesised h,k,l

# Define Q coordinates and HKL for the coordinates.
q1 = [-0.061,2.135,0.00]
q2 = [-0.613,1.277,0.035]
HKL1 = [2,0,2]
HKL2 = [0,0,2]

# this function uses two coordinates in Q space and align them to corrdinates in HKL space
ds.alignToRefs(q1 = q1, q2 = q2, HKL1 = HKL1, HKL2 = HKL2)

# View various things related to calculated UB matrix
print('\nROT')
print(ds[0].sample.ROT)

print('\nP1') 
print(ds[0].sample.P1)
print('P2') 
print(ds[0].sample.P2)
print('P3') 
print(ds[0].sample.P3)

print('\nprojection vectors')
print(ds[0].sample.projectionVectors)

print('\nUB matrix')
print(ds[0].sample.UB)


# To find the A3, A4 and z values of a reflection, we can use calcualteHKLToA3A4Z
# on DMC:
#   A3 = sample rotation angle (degrees) NB: check which axes you're rotating
#   A4 = two theta (degrees)
#   z = vertical position from middle of detector (metres)
# The function work on both DataSet and DataFile level
#
# Syntax is ds.calculateHKLToA3A4Z(h,k,l)


# Make a list of the reflections you want to calculate angles for
my_reflections_list = [[1,1,0],
                       [2,0,2],
                       [4,0,2],
                       [4,0,6],
                       [2,0,-4],
                       [6,0,-4],
                       [2,0,-6],
                       [0,0,6],
                       [4,0,4],
                       [0,0,-4],
                       [10,0,-4]]

# loop to calculate angles for each HKL
# if angles are all numbers: add to a list which becomes the inital dataframe
# if calculated angles contain nans: add to a different list to append to dataframe
my_reflections_A3A4Z_list = []
nan_reflections_list = []
for reflection in my_reflections_list:  
    A3A4Z = ds.calculateHKLToA3A4Z(*reflection) 
    reflection_A3A4Z = [*reflection, *A3A4Z]
    if math.isnan(A3A4Z[0]) or math.isnan(A3A4Z[1]) or math.isnan(A3A4Z[2]):
        nan_reflections_list.append(reflection_A3A4Z)
    else:    
        my_reflections_A3A4Z_list.append(reflection_A3A4Z)

my_reflections_dataframe = pd.DataFrame(np.array(my_reflections_A3A4Z_list),
                                        columns = ['h', 'k', 'l','A3 (deg)','A4 (deg)', 'z (m)'])
for nan_reflection in nan_reflections_list:
    my_reflections_dataframe.loc[len(my_reflections_dataframe)] = nan_reflection

# for whatever mystery reason, 2theta [Wombat] = -A4 [DMC] 
my_reflections_dataframe['two theta (deg)'] = -my_reflections_dataframe['A4 (deg)']

# sort dataframe by two theta
my_reflections_dataframe = my_reflections_dataframe.sort_values(by=['two theta (deg)'])

# view the dataframe of reflections and calculated angles 
print()
print(my_reflections_dataframe)

# save dataframe to spreadsheet
spreadsheet_filename = '{0}_reflections_angles.xlsx'.format(sample_name)
my_reflections_dataframe.to_excel(spreadsheet_filename, float_format = "%.5f")
print('\nsaved hkl and angles to {0} \n'.format(spreadsheet_filename))


