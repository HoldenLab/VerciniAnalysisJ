#@ int	   (label="Time window half-width",description="t-window") tWindow
#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter", value="*.tif") fileFilter
#@ boolean (label = "Search subdirectories", value = true, persist=true) doRecursiveSearch
#@ boolean (label = "Skip *tempFilt*", value = true, persist=true) ignoreFilt
#@ boolean (label = "Skip 'exclude' subdirs", value = true, persist=true) ignoreExcludeDir
# Warning: batch mode breaks if it encounters a bioformats file

from ij import IJ;
import os
import fnmatch
from ij.plugin import ImageCalculator as ic

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
			if ignoreFilt and ("tempFilt" in filename):
				continue
			#check there is a corresponding .roi.zip
			tifPath = os.path.join(root,filename);
			processFile(tifPath);

def processFile(tifPath):

	#open the file
	imp=IJ.openImage(tifPath);
	imp.show();
	imName = imp.title;
	imDir = IJ.getDirectory("image");
	
        
        IJ.run("Conversions...", " "); # ensure that IJ does not rescale when converting 32->16bit

        #Warning - converts to 16 bit! 
        imp=IJ.getImage();
        IJ.run(imp, "16-bit", "");

	IJ.run(imp,"Bleach Correction", "correction=[Exponential Fit]");
	imp_bleachCor = IJ.getImage();
	IJ.run(imp_bleachCor,"Trails", "time="+str(tWindow));
	imp_tSmooth= IJ.getImage();

	IC1 = ic();
	#for come reason ImageCalculator only works if none of the images have had IJ.show applied to them!
	imp_tFilt = IC1.run("Subtract create 32-bit stack",imp_bleachCor,imp_tSmooth);

	#show without brackets fails silently!!
	imp_tFilt.show();
	
	imName_tFilt=imName.replace(".tif",("_tempFilt"+str(tWindow*2+1)+".tif"));
	
	#save the new image
	imPath = os.path.join(imDir,imName_tFilt);
	IJ.saveAsTiff(imp_tFilt,imPath);

	imp.changes= False;#close without confirmation
	imp.close();
	imp_bleachCor.close();
	imp_tFilt.close();
	imp_tSmooth.close();
	IJ.getImage().close();#close the bleaching curve - this might be unreliable

main();
