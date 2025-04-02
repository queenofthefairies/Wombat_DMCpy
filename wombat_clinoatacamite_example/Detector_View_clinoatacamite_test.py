""" wombat DMCpy script for single data files
this script tests functionality of the DMCpy package, wombat edition,

- interactive viewer for looking at raw detector data of a single file

Test data = clinoatacamite dataset 
"""
import sys
# add location of Wombat DMCpy scripts
sys.path.append('J:\wombat_instrument_work\eulerian_cradle\Wombat_DMCpy')
import os
from wombatDMCpy import WombatDataFile, WombatDataSet, _tools
import numpy as np
import matplotlib.pyplot as plt

# sample name (just used when saving figs)
sample_name = 'clinoatacamite' 
# directory where the data are
data_dir = os.getcwd() + '/clinoatacamite_data/'  
# One file at a time please!!!
file_name = 'WBT0100810.nx.hdf' 
# Rotation axis in this case was Euler Omega
sample_rotation_axis = 'eom' 

# Load the data
file_path = data_dir + file_name
df = WombatDataFile.loadWombatDataFile(file_path,
                                       #twoThetaPosition=twoThetaOffset, 
                                       fileType = 'singlecrystal',
                                       wavelength=2.41, # Wavelength in angstroms
                                       radius=0.728, # Wombat sample-detector distance
                                       sampleRotationAxis = sample_rotation_axis)

# Run the interactive detector viewer
IA1 = df.InteractiveViewer(sampleRotationAxis = sample_rotation_axis)
# set colour map limits for detector view
IA1.set_clim(0,20)
# set colour map limits for z integrated data
IA1.set_clim_zIntegrated(0,1000)
# save the figure. You can also save from the matplotlib interactive window.
IA1.fig.savefig('{0}_{1}_{2}_scan_detector_view.png'.format(sample_name,
                                                            file_name[:-7],
                                                            sample_rotation_axis),
                                                            format='png')
plt.show()

# to plot a particular step
step_number = 21
# the function is called "plot spectrum" because it's borrowed from a data 
# visualisation thing for a spectrometer 
# so don't @ me!
IA1.plotSpectrum(index=step_number) 

IA1.fig.savefig('{0}_{1}_{2}_scan_detector_view_step_number_{3}.png'.format(sample_name,file_name[:-7],
                                                                            sample_rotation_axis,
                                                                            step_number),
                                                                            format='png')