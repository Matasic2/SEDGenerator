Original PyCoCo code available [here](https://github.com/maria-vincenzi/PyCoCo_templates).

### Instructions for generating new templates:
1. Change `COCO_PATH` in `Codes_Scripts/config.py`. (only do this once)
1. Add SN peak date into `peak_dicts` dictionary in `Codes_Scripts/a9_Final_Template_SNANAformat.py`.
1. Add `SN_name` in `run.py`
1. Add photometric data into `Inputs/Photometry/0_LCs_mags_raw`. If you are using data from YSE_DR1, you can use `InputGenerator/generate_phot_data.py` to format photometric data.
1. Add SN info into `Inputs/SNe_Info/info.dat`
1. Add Spectroscopic data: 
	1. Add spectroscopy data into `Inputs/Spectroscopy/1_spec_original/(SNNAME)`. You will probably need to create (SNNAME) folder. 
	1. Add a list of spectroscopic data into `Inputs/Spectroscopy/1_spec_lists_original/(SNNAME).list`. You will probably need to create (SNNAME).list file. Columns in the list file are: directory, SN name, observation MJD, redshift (see other .list files for formatting). The first entry in this list must be repeated and entries must be ordered by their observation MJD. Script `Inputs/Spectroscopy/1_spec_original/SN2019yvr/printList.py` could be helpful with generating the .list file.
	1. Check spectroscopic data for negative values and right units. Spectra needs to be non-normalized, calibrated F_lambda spectra in units of erg s⁻¹ cm⁻² Å⁻¹. Usually good y values are between e-15 and e-18. Larger values and negative values are usually indicator of different units (if there are only a few negative values, spectra might still be usable if rows with negative values are deleted). Smoothing can also be applied with `Inputs/Spectroscopy/1_spec_original/SN2019yvr/proc.py`.
1. Add folder in `Outputs` for new SN. Copy `exclude_filt` and `VVBB` from other SN folders in outputs 2019 or later.
1. Use `run.py` to run PyCoCo. Do not use `run.py` in Codes_Scripts folder.
1. Your template should appear in `Templates_HostCorrected` folder. You can use `plotSEDs.ipynb` in `sedCompare` folder to plot your new SED. Use `filterSEDfile` function to filter any NaNs that might exist. 

On Windows, Outputs folder will need to be cleared before re-running the code for SN that already has outputs in Outputs folder (except `exclude_filt` and `VVBB`).
This code has not been tested on other OS.
