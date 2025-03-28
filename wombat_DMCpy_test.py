# wombat DMCpy test file

from DMCpy import WombatDataFile, DataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

# Create a DataFile and DataSet for 

#test_data = 'clinoatacamite'
test_data = 'YSiO'
axis_option = 2

interactive_view = 0
view_3D = 1

if test_data == 'clinoatacamite':
    file = 'wombat_clinoatacamite_data/WBT0100810.nx.hdf'

    # clinoatacamite unit cell 
    unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90])

if test_data == 'YSiO':
    file = 'WBT0102676.nx.hdf'

    # clinoatacamite unit cell 
    unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90])


df = WombatDataFile.loadWombatDataFile(file,
                                       #twoThetaPosition=twoThetaOffset, 
                                       fileType = 'singlecrystal',
                                       #unitCell = unitCell,
                                       wavelength=2.41)

# print()
# print('wavelength')
# print(df.wavelength)
# print()


# print('two theta')
# print(df.twoTheta)
# print()

# print('alpha')
# print(df.alpha)
# print()


#print('A3')
#print(df.A3)
#print()

print('len A3')
print(len(df.A3))
print()

# print('Ki')
# print(df.Ki)
# print()


# run the Interactive Viewer
if interactive_view:
    IA1 = df.InteractiveViewer()
    IA1.set_clim(0,20)
    IA1.set_clim_zIntegrated(0,1000)

    IA1.fig.savefig('figure0.png',format='png')
    plt.show()

    IA1.plotSpectrum(index=21)

    IA1.fig.savefig('figure2a.png',format='png')

if view_3D:
    # Use above data file in data set. Must be inserted as a list
    ds = WombatDataSet.WombatDataSet([df])

    # Viewer3D
    Viewer = ds.Viewer3D(0.01, 0.01, 0.01, rlu = False)

    # Set the color bar limits to 0 and 0.001
    Viewer.set_clim(0,0.001)

    # set axes to be equal
    Viewer.ax.axis('equal')

    # Find the number of steps and set viewer to middle value
    # This can also be done interactively in the viewer by pressing up or down,
    # or by scrolling the mouse wheel or clicking the sliding bar.

    if axis_option == 2:
        zSteps = Viewer.Z.shape[-1]
        print('steps = {0}'.format(zSteps))
        Viewer.setPlane(int(zSteps/2)-1)

        fig = Viewer.ax.get_figure()
        fig.savefig('{0}_figure3D_2.png'.format(test_data),format='png')
        plt.show()
    # Instead of only stepping through the data with the Qx and Qy in the plane
    # one can flip the view by clicking 0, 1, or 2 in the interactive view,
    # or do it programmatically by
    if axis_option == 0:
        #Viewer.changeAxis(0)
        xSteps = Viewer.X.shape[-1]
        Viewer.setPlane(int(xSteps/2)-1)
        print('steps = {0}'.format(xSteps))

        fig = Viewer.ax.get_figure()
        fig.savefig('{0}_figure3D_0.png'.format(test_data),format='png')
        plt.show()

    if axis_option == 1:
        #Viewer.changeAxis(1)
        ySteps = Viewer.Y.shape[-1]
        Viewer.setPlane(int(ySteps/2)-1)
        print('steps = {0}'.format(ySteps))

        fig = Viewer.ax.get_figure()
        fig.savefig('{0}_figure3D_1.png'.format(test_data),format='png')
        plt.show()

    # Notice that the shape of X, Y, and Z changes when the axis is flipped!
    # The last dimension is alway 'orthogonal' to the view.
