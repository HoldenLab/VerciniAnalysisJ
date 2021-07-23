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



Some short test VerCINI data (raw data, and kymographs) is provided to check the plugins work as expected https://github.com/HoldenLab/VerciniAnalysisJ/tree/master/testing


LICENSING INFORMATION

All files are distributed under the GPLv3 and (c) 2020 Seamus Holden, Newcastle University unless otherwise stated. See LICENSE.txt for full terms.

CITATION

If you use this software in work leading to a scientifc publication, please cite: 

FtsZ treadmilling is essential for Z-ring condensation and septal constriction initiation in Bacillus subtilis cell division
Kevin D. Whitley, Calum Jukes, Nicholas Tregidgo, Eleni Karinou, Pedro Almada, Yann Cesbron, Ricardo Henriques, Cees Dekker, Séamus Holden
Nature Communications 12, 2448 (2021). https://doi.org/10.1038/s41467-021-22526-0

