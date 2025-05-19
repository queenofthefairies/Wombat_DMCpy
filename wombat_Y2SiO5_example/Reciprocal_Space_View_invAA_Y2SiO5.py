""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,

- Viewer3D reciprocal space view for datasets containing multiple HDF files
(the idea being you can stitch together many HDF to cover all of reciprocal space)
(Qx, Qy, Qz plotted in inverse Angstroms)

Test data = Y2SiO5 dataset

NB: right now, you can only stitch together HDF files with the same number of steps!
"""
import sys
# add location of Wombat DMCpy scripts
sys.path.append('J:\wombat_instrument_work\eulerian_cradle\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

# sample name (just used when saving figs)
sample_name = 'Y2SiO5'
# directory where the data are
data_dir = os.getcwd() + '/Y2SiO5_data/'
# currently all HDF must be of the same dimension
# here 676 and 677 both have 600 steps but 678 has 601 steps so we leave it out
file_name_list = ['WBT0102676.nx.hdf', 'WBT0102677.nx.hdf']
# Rotation axis in this case was Euler Phi
sample_rotation_axis = 'ephi'

# View 3D axis options, select one
axis_option = 2 # view scattering plane i.e. Qx-Qy plane 
#axis_option = 1 # view out-of-plane Qx-Qz
#axis_option = 0 # view other out-of-plane Qy-Qz

# Load the data
data_file_list = []
for i in range(len(file_name_list)):
    file_name = file_name_list[i]
    file_path = data_dir + file_name
    df = WombatDataFile.loadWombatDataFile(file_path,
                                           #twoThetaPosition=twoThetaOffset, 
                                           fileType = 'singlecrystal',
                                           wavelength=2.41, # Wavelength in angstroms
                                           radius=0.728, # Wombat sample-detector distance
                                           sampleRotationAxis = sample_rotation_axis)
    data_file_list.append(df)

# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

# Run the reciprocal space viewer, Viewer3D
# rlu option is false as we are plotting Qx, Qy, Qz in AA^-1
Viewer = ds.Viewer3D(0.01, 0.01, 0.01, rlu = False)

# Set the color bar limits to 0 and 0.001
Viewer.set_clim(0,0.001)

# set axes to be equal
Viewer.ax.axis('equal')

fileRange_str = ds.fileRange

# this is just to make naming figures when you save them easier
# remember you can also save figs in the interactive matplotlib window
prefix_for_figures = '{0}_{1}_{2}_scan'.format(sample_name,
                                               fileRange_str,
                                               sample_rotation_axis)

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
    fig.savefig('{0}_Qx-Qy_plane.png'.format(prefix_for_figures),format='png')
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
    fig.savefig('{0}_Qy-Qz_plane.png'.format(prefix_for_figures),format='png')
    plt.show()

# Similar thing, changing to the other axis option
if axis_option == 1:
    Viewer.changeAxis(1)
    ySteps = Viewer.Y.shape[-1]
    Viewer.setPlane(int(ySteps/2)-1)
    print('viewing Qz-Qx plane')
    print('Qy steps = {0}'.format(ySteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_Qz-Qx_plane.png'.format(prefix_for_figures),format='png')
    plt.show()