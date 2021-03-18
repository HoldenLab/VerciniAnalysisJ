#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter", value="*.tif") fileFilter
#@ boolean (label = "Search subdirectories", value = true) doRecursiveSearch
# Skips Indiv_rings directories (how to say this on the plugin?)
# Skips files without correspoinding .roi.zip
# Warning: batch mode breaks if it encounters a bioformats file
# updated to disable per ring registration, may be unreliable
#  Batch crop image to rois in associated zip file

from ij import IJ;
from ij.plugin.frame import RoiManager
import os
import fnmatch

def main():
    srcDir = srcFile.getAbsolutePath();
               
    for root, directories, filenames in os.walk(srcDir, topdown=True):
        if not doRecursiveSearch and root != srcDir:
            continue
        #Ignore any directories named "Indiv_rings" 
        directories[:] = [directory for directory in directories if directory != "Indiv_rings"];
        
        for filename in filenames:
            # Check for file name pattern
            if not fnmatch.fnmatch(filename, fileFilter):
                continue
            #Ignore denoised
            #check there is a corresponding .roi.zip
            tifPath = os.path.join(root,filename);
            roiPath = tifPath.replace(".tif",".roi.zip") 
            if not os.path.isfile(roiPath):
                continue
            processFile(tifPath,roiPath);

def processFile(tifPath,roiPath):
    #open the file
    imp = IJ.openImage(tifPath);
    imp.show();
    #clear the roi manager and load the new rois
    rm = RoiManager.getInstance()
    if not rm:
          rm = RoiManager()
    rm.reset();
    rm.runCommand("Open",roiPath);
    #process it    
    cropAllRings();
    imp.close;
    

def cropAllRings():
    def cropRoi(imp,ii,roiName):#duplicate and crop roi
        rm.select(imp,ii);
        IJ.run(imp,"Duplicate...", ("title = "+roiName+" duplicate"));
        impRoi=IJ.getImage();
        return impRoi;
    

    imp = IJ.getImage();
    imName = imp.title;
    imDir = IJ.getDirectory("image");#TODO: check if this returns "None"

    # take the rois, crop and save
    #make an analysis directory
    analysisDir = os.path.join(imDir,"Indiv_rings")
    if not os.path.exists(analysisDir):
        os.makedirs(analysisDir)
        
    rm = RoiManager.getInstance()
    n=rm.count;
    #Test whether there are ROIs in ROI manager
    if (n==0):
        IJ.showMessage("Please draw or load ROIs");
    else:
        for ii in range(0,n):
            roiName = imName.replace(".tif","") +"_ring"+str(ii+1)+".tif";
            impRoi=cropRoi(imp,ii,roiName);
            #save roi
            imPath = os.path.join(analysisDir,roiName);
            IJ.saveAsTiff(impRoi,imPath);
            impRoi.close();

    imp.close();



main();
