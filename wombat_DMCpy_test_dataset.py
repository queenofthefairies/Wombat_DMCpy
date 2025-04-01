""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,
- Viewer3D reciprocal space view for datasets containing multiple HDF files
(the idea being you can stitch together many HDF to cover all of reciprocal space)

Test data: Y2SiO5 dataset
"""

from DMCpy import WombatDataFile, DataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

sample_name = 'Y2SiO5'

# View 3D axis options
axis_option = 2 # view scattering plane i.e. Qx-Qy plane 
#axis_option = 1 # view out-of-plane Qy-Qz
#axis_option = 0 # view other out-of-plane Qz-Qx

data_dir = 'wombat_Y2SiO5_data/'
file_name_list = ['WBT0102676.nx.hdf', 'WBT0102677.nx.hdf', 'WBT0102678.nx.hdf']
sample_rotation_axis = 'ephi'
unit_cell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90]) #[a, b, c, alpha, beta, gamma]

# Load the data
data_file_list = []
for i in range(len(file_name_list)):
    file_name = file_name_list[i]
    file_path = data_dir + file_name
    df = WombatDataFile.loadWombatDataFile(file_path,
                                           #twoThetaPosition=twoThetaOffset, 
                                           fileType = 'singlecrystal',
                                           #unitCell = unitCell,
                                           wavelength=2.41,
                                           radius=0.728, # Wombat sample-detector distance
                                           sampleRotationAxis = sample_rotation_axis)
    data_file_list.append(df)

# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

# Run the reciprocal space viewer, Viewer3D
Viewer = ds.Viewer3D(0.01, 0.01, 0.01, rlu = False)

# Set the color bar limits to 0 and 0.001
Viewer.set_clim(0,0.00001)

# set axes to be equal
Viewer.ax.axis('equal')

# Find the number of steps and set viewer to middle value
# This can also be done interactively in the viewer by pressing up or down,
# or by scrolling the mouse wheel or clicking the sliding bar.

prefix_for_figures = '{0}_{1}-{2}_{3}_scan'.format(sample_name,
                                                   file_name_list[0],
                                                   file_name_list[1],
                                                   sample_rotation_axis)

if axis_option == 2:
    Viewer.changeAxis(2)
    zSteps = Viewer.Z.shape[-1]
    print('viewing Qx-Qy plane')
    print('Qz steps = {0}'.format(zSteps))
    Viewer.setPlane(int(zSteps/2)-1)

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_Qx-Qy_plane.png'.format(prefix_for_figures),format='png')
    plt.show()
# Instead of only stepping through the data with the Qx and Qy in the plane
# one can flip the view by clicking 0, 1, or 2 in the interactive view,
# or do it programmatically by
if axis_option == 0:
    Viewer.changeAxis(0)
    xSteps = Viewer.X.shape[-1]
    Viewer.setPlane(int(xSteps/2)-1)
    print('viewing Qy-Qz plane')
    print('Qx steps = {0}'.format(xSteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_{1}_{2}_scan_Qy-Qz_plane.png'.format(sample_name,file_name[:-7],sample_rotation_axis),format='png')
    plt.show()

if axis_option == 1:
    Viewer.changeAxis(1)
    ySteps = Viewer.Y.shape[-1]
    Viewer.setPlane(int(ySteps/2)-1)
    print('viewing Qz-Qx plane')
    print('Qy steps = {0}'.format(ySteps))

    fig = Viewer.ax.get_figure()
    fig.savefig('{0}_{1}_{2}_scan_Qz-Qx_plane.png'.format(sample_name,file_name[:-7],sample_rotation_axis),format='png')
    plt.show()

# Notice that the shape of X, Y, and Z changes when the axis is flipped!
# The last dimension is alway 'orthogonal' to the view.
