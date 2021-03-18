#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter", value="*.tif") fileFilter
#@ boolean (label = "Search subdirectories", value = true, persist=true) doRecursiveSearch
#@ boolean (label = "Skip *denoise_reg.tif", value = true, persist=true) ignoreDenoised
#@ boolean (label = "Skip 'exclude' subdirs", value = true, persist=true) ignoreExcludeDir
# Warning: batch mode breaks if it encounters a bioformats file
# Batch denoise and register images

from ij import IJ;
import os
import fnmatch

def main():
	srcDir = srcFile.getAbsolutePath();
 	  		
	for root, directories, filenames in os.walk(srcDir, topdown=True):
		if not doRecursiveSearch and root != srcDir:
			continue
                if ignoreExcludeDir:
                    #Ignore any directories named "exclude" 
                    directories[:] = [directory for directory in directories if directory != "exclude"];
		
		for filename in filenames:
    		# Check for file name pattern
			if not fnmatch.fnmatch(filename, fileFilter):
				continue
			#Ignore denoised
			if ignoreDenoised and filename.endswith("denoise_reg.tif"):
				continue
			#check there is a corresponding .roi.zip
			tifPath = os.path.join(root,filename);
			processFile(tifPath);

def processFile(tifPath):

	#open the file
	imp = IJ.openImage(tifPath);
	imp.show();
	
	#denoise and register the entire image
	imp = IJ.getImage();
	imName = imp.title;
	imDir = IJ.getDirectory("image");#TODO: check if this returns "None"
        #record the image size params and add them back to the denoised image
        #because puredenoise currently strips all this info out of the denoised image
        cal = imp.getCalibration();
        unit = cal.unit;
        pix_w = cal.pixelWidth;
        pix_h = cal.pixelHeight;
        timeUnit = cal.timeUnit;
        frameInterval= cal.frameInterval;

	IJ.run(imp,"PureDenoise ...", "parameters='3 4' estimation='Auto Individual' ");
	imp2 = IJ.getImage();
	IJ.run(imp2,"StackReg", "transformation=[Rigid Body]");
	imName2 = imName.replace(".tif","") +"_denoise_reg.tif";
	imp2.title=imName2;
        # Swap Z and T dimensions if T=1
        dims = imp2.getDimensions() # default order: XYCZT
        if (dims[4] == 1):
            imp2.setDimensions( dims[2],dims[4],dims[3] )
        #add the units back to the new image
        cal = imp2.getCalibration();
        cal.unit = unit;
        cal.pixelWidth = pix_w;
        cal.timeUnit = timeUnit;
        cal.frameInterval=frameInterval;
        cal.pixelHeight = pix_h;
            
	#save the new image
	imPath = os.path.join(imDir,imName2);
	IJ.saveAsTiff(imp2,imPath);
	
	imp.close();
	imp2.close();



main();
