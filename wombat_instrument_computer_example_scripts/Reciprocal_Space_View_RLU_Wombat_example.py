# the virtual environment to run this script in is wombatsinglecrystal
""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,

- readCryFileFromInt3D which imports Int3D .cry file with cell parameters and UB matrix

- 3Dalign which lets you specify projection vectors in h,k,l (r.l.u.) for the 3D viewer 

- Viewer3D 
    - this script demonstrates Viewer3D for datasets containing multiple HDF files
      (the idea being you can stitch together many HDF to cover all of reciprocal space)
    - shows reciprocal space in r.l.u. given the UB matrix and projection vectors

Test data: Y2SiO5 dataset
"""
import sys
# add location of Wombat DMCpy scripts, no need to edit this line or the original scripts!
sys.path.append('C:/Users/wombat/wombatDMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
from wombatDMCpy._tools import readCryFileFromInt3D
import numpy as np
import matplotlib.pyplot as plt


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ get the data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# sample name (just used when saving figs)
sample_name = 'Y2SiO5'
# directory where the data are
data_dir = 'data/' #'Z:/cycle/160/data/sics/'
# currently all HDF must be of the same dimension
# here 676 and 677 both have 600 steps but 678 has 601 steps so we leave it out
file_name_list = ['WBT0102676.nx.hdf', 'WBT0102677.nx.hdf']
# Rotation axis options: som, eom, ephi, epsi, msom
# Rotation axis in this case was Euler Phi
sample_rotation_axis = 'ephi'
# need to manually specify wavelength (use None for default of 2.41 Angstroms)
wavelength = 2.41 # Angstroms
# Path to Wombat calibration file (or None)
calibration_file = 'W:/calibration/2025_02/eff_2025_02_27.gumtree.hdf'

# For plotting in r.l.u. you need to supply a unit cell
##### Load .cry file from Int3D with unit cell parameters and UB matrix
unit_cell, int3D_UB_matrix = readCryFileFromInt3D('example_UB_fromInt3D_Y2SiO5.cry')

Qspace_bin_size = 0.01 # in Angstroms, 0.01 for 2.41, 0.02 or 0.025 for shorter wavelength
colourscale_log = False # True = Log scale, or False = Linear scale
colourbar_intensity_min = 0 # set intensity colourscale min and max
colourbar_intensity_max = 0.001
#colourbar_intensity_min = -8 # for log scale need to specify order of magnitude
#colourbar_intensity_max = -3
colourmap = 'viridis' # usual matplotlib options available

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
                                           wavelength=wavelength, # Wavelength in angstroms
                                           radius=0.728, # Wombat sample-detector distance
                                           sampleRotationAxis = sample_rotation_axis,
                                           calibrationFile = calibration_file)
    data_file_list.append(df)

# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

"""~~~~~~ UB Matrix and aligning data to projection vectors in r.l.u. ~~~~~~~"""
# Either you load .cry file (already done above)
# or manually load UB matrix here
#int3D_UB_matrix = np.array([[-0.07128796726465, -0.00493851210922, -0.00514440611005],
#                            [0.04053531959653, -0.00255302991718,  0.11326986551285],
#                            [-0.00167354044970,  0.14852857589722,  0.00177592528053]])

# Most of the time these three angles will be zero!!!
chi_angle_deg = 0.00 # only use if omega scan data acquired with nonzero echi
phi_angle_deg = 0.00 # only use if omega scan data acquired with nonzero ephi
om_angle_deg = 28.00 # only use if phi scan data acquired with nonzero eom

######## Use UB matrix from Int3D 
ds.useUBmatrixFromInt3D(int3D_UB_matrix, 
                        eom = om_angle_deg, 
                        echi = chi_angle_deg, 
                        ephi = phi_angle_deg)

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
Viewer = ds.Viewer3D(Qspace_bin_size, Qspace_bin_size, Qspace_bin_size, rlu = True, log=colourscale_log, cmap=colourmap)

# Set the color bar limits
Viewer.set_clim(colourbar_intensity_min, colourbar_intensity_max)

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

