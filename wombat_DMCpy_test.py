# wombat DMCpy test file

from DMCpy import WombatDataFile, DataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

# Create a DataFile and DataSet for 565
file = 'wombat_clinoatacamite_data/WBT0100810.nx.hdf'

# clinoatacamite unit cell 
unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90])


df = WombatDataFile.loadWombatDataFile(file,
                                       #twoThetaPosition=twoThetaOffset, 
                                       unitCell = unitCell,
                                       wavelength=2.41)

# run the Interactive Viewer
# IA1 = df.InteractiveViewer()
# IA1.set_clim(0,20)
# IA1.set_clim_zIntegrated(0,1000)

#IA1.fig.savefig('figure0.png',format='png')
#plt.show()

#IA1.plotSpectrum(index=21)

#IA1.fig.savefig('figure2a.png',format='png')

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
zSteps = Viewer.Z.shape[-1]
Viewer.setPlane(int(zSteps/2)-1)

fig = Viewer.ax.get_figure()
fig.savefig('figure3D.png',format='png')
plt.show()