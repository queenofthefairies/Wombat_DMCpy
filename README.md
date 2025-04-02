DMCpy x Wombat
============
Python software packaged designed for reduction of single crystal diffraction data from DMC at PSI, now adapted for single crystal data from the high intensity diffractometer Wombat at ANSTO

## What's new for Wombat?
The main differences between PSI / DMC and ANSTO / Wombat are:   
- different HDF file structure (hence new WombatFileStructure)
- different detector geometry and sample rotation options (hence new classes WombatDataFile and WombatDataSet)

Some small tweaks to the functionality of Interactive Viewer (raw detector view) and Viewer 3D (reciprocal space view) have also been made for the Wombat context.

**NB: no work has been done to make the powder diffraction functions of DMCpy compatible with Wombat.** The powder data reduction routine developed by James Hester for Echidna and Wombat is described in [this paper](https://doi.org/10.1107/S1600576718014048) and the current Wombat powder data reduction routine is available from the [Gumtree/Wombat_scripts](https://github.com/Gumtree/Wombat_scripts) github repository

## original DMCpy package
The original DMCpy package was developed by Jakob Lass, Samuel Harrison Moody, and Øystein Slagtern Fjellvåga.

The code is documented [here](https://dmcpy.readthedocs.io/en/latest/index.html) -- this includes tutorials with some examples from DMC at PSI.
For a detailed description see [their arXiv preprint](https://doi.org/10.48550/arXiv.2501.08845) 
and all the code can be found at the github repository [Jakob-Lass/DMCpy](https://github.com/Jakob-Lass/DMCpy) 

### Installation of original DMCpy package
The original DMCpy package can be installed through the Python Package Manager by issuing 

```
pip install DMCpy
```


