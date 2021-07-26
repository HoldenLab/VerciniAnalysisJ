# VerciniAnalysisJ

INFORMATION This is a set of ImageJ scripts for analysis of VerCINI (Vertical Cell Imaging by Nanostructured Immobilization) data First published in Whitley et al, bioRxiv 2020. 
This software is provided as is and without warranty.

OVERVIEW

SYSTEM REQUIREMENTS

This package does not require any special hardware. However, for large datasets a large amount of RAM will be required for denoising. We recommmend >16 GB of RAM for optimal performance.

This package development system has been tested on Windows 10, but should be compatible with other operating systems.

The only software required is FIJI.

INSTALLATION

Install the VerciniAnalysisJ plugin in FIJI by 
- Clicking Help > Update > Manage Update Sites > VerciniAnalysisJ. 
- Close "Manage Update Sites" dialog and click "Apply changes"
This should install the plugin and all dependencies within ~1 min.

USAGE INSTRUCTIONS

Open Fiji, start the plugin by running Plugins > VerciniAnalysisJ > Start Vercini ActionBar. Denoising may take >30 min for large datasets. Registration may take 5-15 min, also depending on the size of the dataset. All other operations should finish within 1 min.

DEMO

Some short test VerCINI data (videos and kymographs) are provided to check the plugins work as expected https://github.com/HoldenLab/VerciniAnalysisJ/tree/master/testing

To test-analyse the videos provided, one option is:
- Open VerciniAnalysisJ ActionBar.
- Draw a 60x60 ROI around the ring in the video and save to ImageJ ROI manager by pressing 't'.
- Save ROIs.
- Use Batch denoise+register+crop. Navigate to the directory containing both the video and compressed ROI file.

The output will be denoised and registered version of the original video (file_denoise_reg.tif), and a directory Indiv_rings containing the cropped ring (file_denoise_reg_ring1.tif).

To test-analyse the kymographs provided, one option is:
- Open VerciniAnalysisJ ActionBar.
- Use Ridge filter with a smoothing scale of 2 pix.
- Use the straight line tool in ImageJ to trace lines, pressing 't' to add them to ROI manager.
- Save the ROIs using the ROI manager window by going to More>Save... and saving them in the same directory as the kymograph with the same file name (e.g. if the kymograph is 180327_mNG-ftsz1_kymoWrap.tif, save the ROI file as 180327_mNG-ftsz1_kymoWrap.zip).
- In VerciniAnalysisJ ActionBar, use Batch kymotrace statistics. Nativate to the directory containing both the video and compressed ROI file.

The output will be a csv file containing the track numbers with lengths, times, speeds, and angles.


LICENSING INFORMATION

All files are distributed under the GPLv3 and (c) 2020 Seamus Holden, Newcastle University unless otherwise stated. See LICENSE.txt for full terms.

CITATION

If you use this software in work leading to a scientifc publication, please cite: 

FtsZ treadmilling is essential for Z-ring condensation and septal constriction initiation in Bacillus subtilis cell division
Kevin D. Whitley, Calum Jukes, Nicholas Tregidgo, Eleni Karinou, Pedro Almada, Yann Cesbron, Ricardo Henriques, Cees Dekker, Séamus Holden
Nature Communications 12, 2448 (2021). https://doi.org/10.1038/s41467-021-22526-0

