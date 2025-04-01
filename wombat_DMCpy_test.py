# wombat DMCpy test file

from DMCpy import WombatDataFile, DataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt



test_data = 'clinoatacamite'
#test_data = 'YSiO'

# Either turn on interactive view or view 3D (not both)
interactive_view = 1 # turn on interactive view (raw detector data)
view_3D = 0 # turn on 3D reciprocal space view 

# View 3D axis options
axis_option = 2 # view scattering plane i.e. Qx-Qy plane 
#axis_option = 1 # view out-of-plane Qy-Qz
#axis_option = 0 # view other out-of-plane Qz-Qx

if test_data == 'clinoatacamite':
    data_dir = 'wombat_clinoatacamite_data/'
    file_name = 'WBT0100810.nx.hdf'
    sample_rotation_axis = 'eom'
    unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90]) #[a, b, c, alpha, beta, gamma]

if test_data == 'YSiO':
    data_dir = ''
    file_name = 'WBT0102676.nx.hdf'
    sample_rotation_axis = 'ephi'
    unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90]) #[a, b, c, alpha, beta, gamma]

# Load the data
file_path = data_dir + file_name
df = WombatDataFile.loadWombatDataFile(file_path,
                                       #twoThetaPosition=twoThetaOffset, 
                                       fileType = 'singlecrystal',
                                       #unitCell = unitCell,
                                       wavelength=2.41,
                                       radius=0.728, # Wombat sample-detector distance
                                       sampleRotationAxis = sample_rotation_axis)


# run the Interactive Viewer
if interactive_view:
    IA1 = df.InteractiveViewer(sampleRotationAxis = sample_rotation_axis)
    # set colour map limits for detector view
    IA1.set_clim(0,20)
    # set colour map limits for z integrated data
    IA1.set_clim_zIntegrated(0,1000)

    IA1.fig.savefig('{0}_{1}_{2}_scan_detector_view.png'.format(test_data,file_name[:-7],
                                                                sample_rotation_axis),
                                                                format='png')
    plt.show()

    # to plot a particular step
    step_number = 21
    IA1.plotSpectrum(index=step_number)

    IA1.fig.savefig('{0}_{1}_{2}_scan_detector_view_step_number_{3}.png'.format(test_data,file_name[:-7],
                                                                                sample_rotation_axis,
                                                                                step_number),
                                                                                format='png')

# run the 3D reciprocal space viewer
if view_3D:
    # Use above data file in data set. Must be inserted as a list
    ds = WombatDataSet.WombatDataSet([df])

    # Viewer3D
    Viewer = ds.Viewer3D(0.01, 0.01, 0.01, rlu = False)

    # Set the color bar limits to 0 and 0.001
    Viewer.set_clim(0,0.00001)

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
        fig.savefig('{0}_{1}_{2}_scan_Qx-Qy_plane.png'.format(test_data,file_name[:-7],sample_rotation_axis),format='png')
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
        fig.savefig('{0}_{1}_{2}_scan_Qy-Qz_plane.png'.format(test_data,file_name[:-7],sample_rotation_axis),format='png')
        plt.show()

    if axis_option == 1:
        Viewer.changeAxis(1)
        ySteps = Viewer.Y.shape[-1]
        Viewer.setPlane(int(ySteps/2)-1)
        print('viewing Qz-Qx plane')
        print('Qy steps = {0}'.format(ySteps))

        fig = Viewer.ax.get_figure()
        fig.savefig('{0}_{1}_{2}_scan_Qz-Qx_plane.png'.format(test_data,file_name[:-7],sample_rotation_axis),format='png')
        plt.show()

    # Notice that the shape of X, Y, and Z changes when the axis is flipped!
    # The last dimension is alway 'orthogonal' to the view.
