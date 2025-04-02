""" wombat DMCpy test script for data sets
this script tests functionality of the DMCpy package, wombat edition,
- Viewer3D reciprocal space view for datasets containing multiple HDF files
(the idea being you can stitch together many HDF to cover all of reciprocal space)

Test data: Y2SiO5 dataset
"""

from DMCpy import WombatDataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

sample_name = 'Y2SiO5'

data_dir = 'wombat_Y2SiO5_data/'
# currently all HDF must be of the same dimension
file_name_list = ['WBT0102676.nx.hdf', 'WBT0102677.nx.hdf']#, 'WBT0102678.nx.hdf']
sample_rotation_axis = 'ephi'
unit_cell = np.array([14.406, 6.728, 10.421, 90, 122.194, 90]) #[a, b, c, alpha, beta, gamma]

# Load the data
data_file_list = []
for i in range(len(file_name_list)):
    file_name = file_name_list[i]
    file_path = data_dir + file_name
    df = WombatDataFile.loadWombatDataFile(file_path,
                                           #twoThetaPosition=twoThetaOffset, 
                                           fileType = 'singlecrystal',
                                           unitCell = unit_cell,
                                           wavelength=2.41,
                                           radius=0.728, # Wombat sample-detector distance
                                           sampleRotationAxis = sample_rotation_axis)
    data_file_list.append(df)

# Use above data files in data set. Must be inserted as a list
ds = WombatDataSet.WombatDataSet(data_file_list)

# Define Q coordinates and HKL for the coordinates.
q1 = [-0.061,2.135,0.00]
q2 = [-0.613,1.277,0.035]
HKL1 = [2,0,2]
HKL2 = [0,0,2]

# this function uses two coordinates in Q space and align them to corrdinates in HKL space
ds.alignToRefs(q1 = q1, q2 = q2, HKL1 = HKL1, HKL2 = HKL2)

# define 2D cut width orthogonal to cut plane
width = 0.5 # in AA^-1

# these points define the plane that will be cut
points = np.array([[0.0,0.0,0.0],
     [1.0,0.0,0.0],
     [0.0,0.0,1.0]])

plane_name = 'h0l'

kwargs = {
   'dQx' : 0.01,
   'dQy' : 0.01,
   'steps' : 10,
   'rlu' : True,
   'rmcFile' : True,
   'colorbar' : True,
   }

ax,returndata,bins = ds.plotQPlane(points=points,width=width,**kwargs)

ax.set_clim(0,0.0001)

plane_fig_name = '{0}_{1}-{2}_{3}_plane.png'.format(sample_name,
                                                    file_name_list[0][:-7],
                                                    file_name_list[-1][:-7],
                                                    plane_name)

plt.savefig(plane_fig_name,format='png')
# we can enforce new projection vectors by this command:
#p1 = np.array([1,0,0])
#p2 = np.array([0,0,1])
#ds.setProjectionVectors(p1,p2,p3=None)



