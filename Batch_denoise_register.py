#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter", value="*.tif") fileFilter
#@ boolean (label = "Search subdirectories", value = true, persist=true) doRecursiveSearch
#@ boolean (label = "Skip *denoise_reg.tif", value = true, persist=true) ignoreDenoised
#@ boolean (label = "Skip 'exclude' subdirs", value = true, persist=true) ignoreExcludeDir
# Warning: batch mode breaks if it encounters a bioformats file

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
	IJ.run(imp,"PureDenoise ...", "parameters='3 4' estimation='Auto Individual' ");
	imp2 = IJ.getImage();
	IJ.run(imp2,"StackReg", "transformation=[Rigid Body]");
	imName2 = imName.replace(".tif","") +"_denoise_reg.tif";
	imp2.title=imName2;
	#save the new image
	imPath = os.path.join(imDir,imName2);
	IJ.saveAsTiff(imp2,imPath);
	

	imp.close();
	imp2.close();



main();
