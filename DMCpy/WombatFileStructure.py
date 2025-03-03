import numpy as np
from collections import defaultdict
import warnings, os
import h5py as hdf


HDFCounts = 'entry1/data/hmm_xy'
HDFCountsBG = None #'entry1/data/background'
## Dictionary for holding hdf position of attributes. HDFTranslation['a3'] gives hdf position of 'a3'
HDFTranslation = {'sample':'/entry1/sample',
                  'sampleName':'/entry1/sample/name', 
                  'monitor':'entry1/monitor',
                  'monitor1':'entry1/monitor/bm1_counts',
                  'unitCell':None, #'/entry1/sample/unit_cell',
                  #'counts':'entry1/DMC/detector/data',
                  #'background':'entry1/DMC/detector/background',
                  #'backgroundType':'entry1/data/backgroundType',
                  'summedCounts': 'entry1/data/total_counts',
                  #'monochromatorCurvature':None,#'entry1/DMC/monochromator/curvature',
                  #'monochromatorVerticalCurvature':None,#'entry1/DMC/monochromator/curvature_vertical',
                  #'monochromatorGoniometerLower':None,#'entry1/DMC/monochromator/goniometer_lower',
                  #'monochromatorGoniometerUpper':None,#'entry1/DMC/monochromator/goniometer_upper',
                  'monochromatorRotationAngle':'entry1/instrument/crystal/rotate',
                  'monochromatorTakeoffAngle':'entry1/instrument/crystal/takeoff_angle',
                  #'monochromatorTranslationLower':'entry1/instrument/crystal/translation_x',
                  #'monochromatorTranslationUpper':'entry1/instrument/crystal/translation_y',
                  
                  'verticalPosition':'entry1/data/y_pixel_offset',
                  #'wavelength':None,#'entry1/DMC/monochromator/wavelength',
                  #'wavelength_raw':None,#'entry1/DMC/monochromator/wavelength_raw',
                  'twoThetaPosition':'entry1/sample/azimuthal_angle',
                  #'mode':None,#'entry1/monitor/mode',
                  #'preset':None,#'entry1/monitor/preset',
                  'startTime':'entry1/start_time',
                  'time':'entry1/monitor/time',#'Henning',# Is to be caught by HDFTranslationAlternatives 'entry1/monitor/time',
                  'endTime':'entry1/end_time',
                  #'comment':None,#'entry1/comment',
                  'proposal':'entry1/sample/name',
                  'proposalTitle':'entry1/sample/description',
                  #'localContact':'entry1/local_contact/name',
                  #'proposalUser':'entry1/proposal_user/name',
                  #'proposalEmail':'entry1/proposal_user/email',
                  'user':'entry1/user/name',
                  'email':'entry1/user/email',
                  #'address':None,#'entry1/user/address',
                  #'affiliation':None,#'entry1/user/affiliation',
                  'A3':'entry1/sample/euler_omega',
                  #'se_r':None,#'entry1/sample/se_r', # this is sample environment rotation axes
                  #'temperature':None,#'entry1/sample/temperature',
                  #'magneticField':None,#'entry1/sample/magnetic_field',
                  #'electricField':None,#'entry1/sample/electric_field',
                  #'scanCommand':None,#'entry1/scancommand',
                  'title':'entry1/sample/short_title',#'entry1/title',
                  #'absoluteTime':None,#'entry1/control/absolute_time',
                  #'protonBeam':None# 'entry1/proton_beam/data'
}

HDFTranslationAlternatives = { # Alternatives to the above list. NOTTICE: The above positions are not checked if an entry in HDFTranslationAlternatives is present
    'time':['entry1/monitor/time'],
    'monitor':['entry1/monitor/bm2_counts']
    #'protonBeam':['entry1/proton_beam/data','entry1/monitor/proton_charge']
}

## Dictionary for holding standard values 

HDFTranslationDefault = {'twoThetaPosition':np.array([0.0]),
                         'comment': 'No Comments',
                         'endTime': '20yy-mm-dd hh:mm:ss',
                         'proposalTitle': 'Unknown Title',
                         'localContact': 'Unknown Local Contact',
                         'proposalUser': 'Unknown User',
                         'proposalEmail': 'Unknown Email',
                         'address': 'Unknown Address',
                         'affiliation': 'Unknown Affiliation',
                         'scanCommand': 'Unknown scanCommand',

                         'wavelength_raw':np.array([2.0]),
                         'monitor1':np.array([0.0]),

                         'temperature': np.array([0.0]),
                         'magneticField': np.array([0.0]),
                         'electricField': np.array([0.0]),

                         'absoluteTime': np.array([0.0]),
                         'protonBeam': np.array([0.0]),
                         'se_r': np.array([0.0]),

                         'backgroundType': 'None'
                         
                         

}

## Default dictionary to perform on loaded data, i.e. take the zeroth element, swap axes, etc

HDFTranslationFunctions = defaultdict(lambda : [])
HDFTranslationFunctions['sampleName'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['mode'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['startTime'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['wavelength'] = [['mean',[]]]
HDFTranslationFunctions['wavelength_raw'] = [['mean',[]]]
HDFTranslationFunctions['twoThetaPosition'] = [['__getitem__',[0]]]
HDFTranslationFunctions['endTime'] = [['__getitem__',[0]]]
HDFTranslationFunctions['experimentalIdentifier'] = [['__getitem__',[0]]]
HDFTranslationFunctions['comment'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['proposal'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['proposalTitle'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['localContact'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['proposalUser'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['proposalEmail'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['user'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['email'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['address'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['affiliation'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['scanCommand'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['title'] = [['__getitem__',[0]],['decode',['utf8']]]
HDFTranslationFunctions['backgroundType'] = [['__getitem__',[0]],['decode',['utf8']]]



HDFInstrumentTranslation = {
}

HDFInstrumentTranslationFunctions = defaultdict(lambda : [])
# HDFInstrumentTranslationFunctions['counts'] = [['swapaxes',[1,2]]]
HDFInstrumentTranslationFunctions['twoThetaPosition'] = [['mean',]]
HDFInstrumentTranslationFunctions['wavelength'] = [['mean',]]
HDFInstrumentTranslationFunctions['wavelength_raw'] = [['mean',]]

extraAttributes = ['name','fileLocation']

possibleAttributes = list(HDFTranslation.keys())+list(HDFInstrumentTranslation.keys())+extraAttributes
possibleAttributes.sort(key=lambda v: v.lower())

HDFTypes = defaultdict(lambda: lambda x: np.array([np.string_(x)]))
HDFTypes['monitor'] = np.array
HDFTypes['monitor1'] = np.array
HDFTypes['monochromatorCurvature'] = np.array
HDFTypes['monochromatorVerticalCurvature'] = np.array
HDFTypes['monochromatorGoniometerLower'] = np.array
HDFTypes['monochromatorGoniometerUpper'] = np.array
HDFTypes['monochromatorRotationAngle'] = np.array
HDFTypes['monochromatorTakeoffAngle'] = np.array
HDFTypes['monochromatorTranslationLower'] = np.array
HDFTypes['monochromatorTranslationUpper'] = np.array
HDFTypes['wavelength'] = np.array
HDFTypes['wavelength_raw'] = np.array
HDFTypes['twoThetaPosition'] = np.array
# HDFTypes['mode'] = lambda x: np.array([np.string_(x)])
HDFTypes['preset'] = np.array
# HDFTypes['startTime'] = np.string_
HDFTypes['time'] = np.array
# HDFTypes['endTime'] = np.string_
# HDFTypes['comment'] = np.string_
HDFTypes['absoluteTime'] = np.array
HDFTypes['protonBeam'] = np.array


HDFUnits = {
    'monitor':'counts',
    'monochromatorCurvature':'degree',
    'monochromatorVerticalCurvature':'degree',
    'monochromatorGoniometerLower':'degree',
    'monochromatorGoniometerUpper':'degree',
    'monochromatorRotationAngle':'degree',
    'monochromatorTakeoffAngle':'degree',
    'monochromatorTranslationLower':'mm',
    'monochromatorTranslationUpper':'mm',
    'twoThetaPosition':'degree',
    'monitor':'counts',
    'monitor1':'counts',
    'protonBeam':'uA',
    'wavelength':'A',
    'wavelength_raw':'A'
}

def getNX_class(x,y,attribute):
    try:
        variableType = y.attrs['NX_class']
    except:
        variableType = ''
    if variableType==attribute:
        return x

def getInstrument(file):
    location = file.visititems(lambda x,y: getNX_class(x,y,b'NXinstrument'))
    return file.get(location)

def shallowRead(files,parameters):

    parameters = np.array(parameters)
    values = []
    possibleAttributes.sort(key=lambda v: v.lower())
    possible = []
    for p in parameters:
        possible.append(p in possibleAttributes)
    
    if not np.all(possible):
        if np.sum(np.logical_not(possible))>1:
            raise AttributeError('Parameters {} not found'.format(parameters[np.logical_not(possible)]))
        else:
            raise AttributeError('Parameter {} not found'.format(parameters[np.logical_not(possible)]))
    
    for file in files:
        vals = {}
        vals['file'] = file
        with hdf.File(file,mode='r') as f:
            instr = getInstrument(f)
            for p in parameters:
                if p == 'name':
                    v = os.path.basename(file)
                    vals[p] = v
                    continue
                elif p == 'fileLocation':
                    v = os.path.dirname(file)
                    vals[p] = v
                    continue
                elif p in HDFTranslationAlternatives:
                    for entry in HDFTranslationAlternatives[p]:
                        v = np.array(f.get(entry))
                        if not v.shape == ():
                            TrF= HDFTranslationFunctions
                            break

                elif p in HDFTranslation:
                    v = np.array(f.get(HDFTranslation[p]))
                    TrF= HDFTranslationFunctions
                elif p in HDFInstrumentTranslation:
                    v = np.array(instr.get(HDFInstrumentTranslation[p]))
                    TrF= HDFInstrumentTranslationFunctions
                else:
                    raise AttributeError('Parameter "{}" not found'.format(p))
                for func,args in TrF[p]:
                    try:
                        v = getattr(v,func)(*args)
                    except (IndexError,AttributeError):
                        warnings.warn('Parameter "{}" not found in file "{}"'.format(p,file))
                        v = None
                        
                vals[p] = v
        values.append(vals)

    return values