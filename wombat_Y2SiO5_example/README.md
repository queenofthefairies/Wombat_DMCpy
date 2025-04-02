# Wombat Y2SiO5 example
This is an example of wombatdmcpy     
- interactive detective viewer `Detector_View_Y2SiO5.py`     
- reciprocal space view (inverse Angstrom) using multiple HDF files `Reciprocal_Space_View_invAA_Y2SiO5.py`  
- using the above, I indexed some peaks by hand and put them in `reciprocal_space_conversion_Y2SiO5.xlsx`        
- reciprocal space view (r.l.u., UB matrix calculated, projection vectors of your choice) `Reciprocal_Space_View_3Dalign_Y2SiO5.py`      

Long scans covering 60 degrees in Euler psi, we knew the scattering plane was approximately *h0l*

Thanks to Federico for the ginormous crystal!

## To do
- can't currently combine HDF with different numbers of steps and different Euler angles       
- cut2D doesn't work (either runs out of memory, or if fewer steps specified then boolean mask size mismatch with data array)     
- longer term, apply vanadium efficiency calibration and tweak normalisation corrections




