# wombat DMCpy test file

from DMCpy import WombatDataFile, DataFile, DataSet, _tools
import numpy as np

# Create a DataFile and DataSet for 565
file = 'wombat_clinoatacamite_data/WBT0100810.nx.hdf'

#df = WombatDataFile.loadWombatDataFile(file)
#ds = DataSet.DataSet(df)

# Create a DataFile and DataSet with _tools.fileListGenerator
#twoThetaOffset = 11.0
# scanNumbers = 'WBT0100810.nx.hdf'
# folder = 'wombat_clinoatacamite_data'
# year = 2025

# clinoatacamite unit cell 
unitCell = np.array([6.144, 6.805, 9.112, 90, 99.55, 90])

# # Create complete filepath
# file = os.path.join(os.getcwd(),_tools.fileListGenerator(scanNumbers,year=year,folder)[0])

df = WombatDataFile.loadWombatDataFile(file,
                                       #twoThetaPosition=twoThetaOffset, 
                                       unitCell = unitCell)

# run the Interactive Viewer
IA1 = df.InteractiveViewer()
IA1.set_clim(0,20)
IA1.set_clim_zIntegrated(0,1000)
# ds = DataSet.DataSet(df)

# If we want to load several DataFiles in the DataSet
#dataFiles = [DataFile.loadDataFile(dFP,twoThetaPosition=twoThetaOffset) for dFP in _tools.fileListGenerator(scanNumbers,folder)]

#ds = DataSet.DataSet(dataFiles)


# We can also add a unit cell to the dataFiles when loaded:
#scanNumbers = '12153'
#folder = 'data/SC'


#filePath = _tools.fileListGenerator(scanNumbers,folder,year=year)



# # # load dataFiles
#dataFiles = [DataFile.loadDataFile(dFP,unitCell = unitCell) for dFP in filePath]