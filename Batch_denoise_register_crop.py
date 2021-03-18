#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter", value="*.tif") fileFilter
#@ boolean (label = "Search subdirectories", value = true) doRecursiveSearch
#@ boolean (label = "Skip *denoise_reg.tif", value = true, persist=true) ignoreDenoised
# Skips Indiv_rings directories (how to say this on the plugin?)
# Skips files without correspoinding .roi.zip
# Warning: batch mode breaks if it encounters a bioformats file
# Batch denoise and register entire image, then crop all associated sub image rois in zip file

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
            if ignoreDenoised and filename.endswith("denoise_reg.tif"):
                continue
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
    preprocessRingFOV();
    imp.close;
    

def preprocessRingFOV():
    def cropRoi(imp,ii,roiName):#duplicate and crop roi
        rm.select(imp,ii);
        IJ.run(imp,"Duplicate...", ("title = "+roiName+" duplicate"));
        impRoi=IJ.getImage();
        return impRoi;
    

    #denoise and register the entire image
    imp = IJ.getImage();
    #record the image size params and add them back to the denoised image
    cal = imp.getCalibration();
    unit = cal.unit;
    pix_w = cal.pixelWidth;
    pix_h = cal.pixelHeight;
    timeUnit = cal.timeUnit;
    frameInterval= cal.frameInterval;


    imName = imp.title;
    imDir = IJ.getDirectory("image");#TODO: check if this returns "None"
    IJ.run(imp,"PureDenoise ...", "parameters='3 4' estimation='Auto Individual' ");

    imp2 = IJ.getImage();
    IJ.run(imp2,"StackReg", "transformation=[Rigid Body]");
    imName2 = imName.replace(".tif","") +"_denoise_reg.tif";
    imp2.title=imName2;
    #fix the screwed up image dimensions introduced by puredenoise
    # Swap Z and T dimensions if T=1
    dims = imp2.getDimensions() # default order: XYCZT
    if (dims[4] == 1):
        imp2.setDimensions( dims[2],dims[4],dims[3] )
    #add the units back to the new image
    cal = imp2.getCalibration();
    cal.unit = unit;
    cal.pixelWidth = pix_w;
    cal.pixelHeight = pix_h;
    cal.timeUnit = timeUnit;
    cal.frameInterval=frameInterval;

    
    #save the new image
    imPath = os.path.join(imDir,imName2);
    IJ.saveAsTiff(imp2,imPath);
    

    # take the rois, crop, register and save
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
            roiName = imName2.replace(".tif","") +"_ring"+str(ii+1)+".tif";
            impRoi=cropRoi(imp2,ii,roiName);
            #save roi
            imPath = os.path.join(analysisDir,roiName);
            IJ.saveAsTiff(impRoi,imPath);
            impRoi.close();

    imp.close();
    imp2.close();



main();
