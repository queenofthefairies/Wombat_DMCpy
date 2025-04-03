""" wombat DMCpy test script for single data files
this script tests functionality of the DMCpy package, wombat edition,

- viewer3D for reciprocal space view for datasets containing just one HDF file
(Qx, Qy, Qz plotted in inverse Angstroms)

Test data = Alex mysterious ND crystal dataset 
"""
import sys
# add location of Wombat DMCpy scripts
sys.path.append('J:\wombat_instrument_work\eulerian_cradle\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt


# sample name (just used when saving figs)
sample_name = 'alex_ND_crystal' 
# directory where the data are
data_dir = os.getcwd() + '/alex_ND_crystal_data/'  
# One file at a time please!!!
file_name = 'WBT0102665.nx.hdf' 
# Rotation axis in this case was sample Omega
sample_rotation_axis = 'som' 

# View 3D axis options, select one
axis_option = 2 # view scattering plane i.e. Qx-Qy plane 
#axis_option = 1 # view out-of-plane Qy-Qz
#axis_option = 0 # view other out-of-plane Qz-Qx

# Load the data
file_path = data_dir + file_name
df = WombatDataFile.loadWombatDataFile(file_path,
                                       #twoThetaPosition=twoThetaOffset, 
                                       fileType = 'singlecrystal',
                                       wavelength=2.41, # Wavelength in angstroms
                                       radius=0.728, # Wombat sample-detector distance
                                       sampleRotationAxis = sample_rotation_axis)

# run the 3D reciprocal space viewer
# Use above data file in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet([df])

# Viewer3D
# rlu option is false as we are plotting Qx, Qy, Qz in AA^-1
Viewer = ds.Viewer3D(0.02, 0.02, 0.02, rlu = False)

# Set the color bar limits to 0 and 0.001
Viewer.set_clim(0,0.0001)

# set axes to be equal
Viewer.ax.axis('equal')

# Find the number of steps and set viewer to middle value
# This can also be done interactively in the viewer by pressing up or down,
# or by scrolling the mouse wheel or clicking the sliding bar.
if axis_option == 2:
    Viewer.changeAxis(2)
    zSteps = Viewer.Z.shape[-1]
    print('viewing Qx-Qy plane')
    print('Qz steps = {0}'.format(zSteps))
    Viewer.setPlane(int(zSteps/2)-1)

    fig = Viewer.ax.get_figure()
    # save the figure. You can also save from the matplotlib interactive window.
    fig.savefig('{0}_{1}_{2}_scan_Qx-Qy_plane.png'.format(sample_name,file_name[:-7],sample_rotation_axis),format='png')
    plt.show()

# Instead of only stepping through the data with the Qx and Qy in the plane
# one can flip the view by clicking 0, 1, or 2 in the interactive view,
# or do it programmatically by Viewer.changeAxis(1) etc.
# Notice that the shape of X, Y, and Z changes when the axis is flipped!
# The last dimension is alway 'orthogonal' to the view.
if axis_option == 0:
    Viewer.changeAxis(0)
    xSteps = Viewer.X.shape[-1]
    Viewer.setPlane(int(xSteps/2)-1)
    print('viewing Qy-Qz plane')
    print('Qx steps = {0}'.format(xSteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_{1}_{2}_scan_Qy-Qz_plane.png'.format(sample_name,file_name[:-7],sample_rotation_axis),format='png')
    plt.show()

# Similar thing, changing to the other axis option
if axis_option == 1:
    Viewer.changeAxis(1)
    ySteps = Viewer.Y.shape[-1]
    Viewer.setPlane(int(ySteps/2)-1)
    print('viewing Qz-Qx plane')
    print('Qy steps = {0}'.format(ySteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_{1}_{2}_scan_Qz-Qx_plane.png'.format(sample_name,file_name[:-7],sample_rotation_axis),format='png')
    plt.show()