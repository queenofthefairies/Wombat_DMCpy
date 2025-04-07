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
sys.path.append('J:\wombat_instrument_work\eulerian_cradle\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
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
q1 = [-1.714,-0.4618,-0.069]
q2 = [-3.971,-1.7614,-0.144]
HKL1 = [4,0,-2]
HKL2 = [4,0,4]

# this function uses two coordinates in Q space and align them to corrdinates in HKL space
ds.alignToRefs(q1 = q1, q2 = q2, HKL1 = HKL1, HKL2 = HKL2)


"""~~~~~~~~~~~~~~~~~~ Reciprocal space viewer in r.l.u. ~~~~~~~~~~~~~~~~~~~~~"""
# Note: for not-orthogonal unit cells, you will have to "add up" the x and y
# co-ordinates in r.l.u. to get the "real" h, k, l (i.e. not simply read off the axes)
# or move your mouse over the plot in the interactive matplotlib window, and in
# the bottom right corner, the "real" h, k, l values of where your cursor is
# will be reported

# we can enforce new projection vectors by this command
# with this choice of p1 and p2 we will get the h0l plane
p1 = np.array([1,0,0])
p2 = np.array([0,0,1])
ds.setProjectionVectors(p1,p2,p3=None)
plane_name = 'h0l' # name for the plane

# Run the reciprocal space viewer, Viewer3D
Viewer = ds.Viewer3D(0.01, 0.01, 0.01, rlu = True)

# Set the color bar limits to 0 and 0.01
Viewer.set_clim(0,0.01)

# set axes to be equal
Viewer.ax.axis('equal')

# this is just to make naming figures when you save them easier
# remember you can also save figs in the interactive matplotlib window
fileRange_str = ds.fileRange
prefix_for_figures = '{0}_{1}_{2}_scan'.format(sample_name,
                                               fileRange_str,
                                               sample_rotation_axis)

########## View plane defined by your projection vectors           
# Find the number of steps and set viewer to middle value
# This can also be done interactively in the viewer by pressing up or down,
# or by scrolling the mouse wheel or clicking the sliding bar.
if axis_option == 2:
    zSteps = Viewer.Z.shape[-1]
    print('viewing {0} plane'.format(plane_name))
    print('Qz steps = {0}'.format(zSteps))
    Viewer.setPlane(int(zSteps/2)-1)

    fig = Viewer.ax.get_figure()
    # save the figure. You can also save from the matplotlib interactive window.
    fig.savefig('{0}_{1}_plane_rlu_true.png'.format(prefix_for_figures,plane_name),format='png')
    plt.show()

########## You can also look orthogonal to the plane defined by your projection vectors in r.l.u.
# Instead of only stepping through the data with the Qx and Qy in the plane
# one can flip the view by clicking 0, 1, or 2 in the interactive view,
# or do it programmatically by Viewer.changeAxis(1) etc.
# Notice that the shape of X, Y, and Z changes when the axis is flipped!
# The last dimension is alway 'orthogonal' to the view.
if axis_option == 0:
    Viewer.changeAxis(0)
    xSteps = Viewer.X.shape[-1]
    Viewer.setPlane(int(xSteps/2)-1)
    print('viewing plane 1 orthogonal to {0} plane'.format(plane_name))
    print('Qx steps = {0}'.format(xSteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_orthogonal_1_to_{1}_plane_rlu_true.png'.format(prefix_for_figures,plane_name),format='png')
    plt.show()

########## The other plane orthogonal to the plane defined by your projection vectors in r.l.u.
if axis_option == 1:
    Viewer.changeAxis(1)
    ySteps = Viewer.Y.shape[-1]
    Viewer.setPlane(int(ySteps/2)-1)
    print('viewing plane 2 orthogonal to {0} plane'.format(plane_name))
    print('Qy steps = {0}'.format(ySteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_orthogonal_2_to_{1}_plane_rlu_true.png'.format(prefix_for_figures,plane_name),format='png')
    plt.show()

