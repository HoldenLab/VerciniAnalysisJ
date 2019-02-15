from ij import IJ;
from ij.plugin.frame import RoiManager
import os

def preprocessRingFOV():
	def cropRoi(imp,ii,roiName):#duplicate and crop roi
		rm.select(imp,ii);
		IJ.run(imp,"Duplicate...", ("title = "+roiName+" duplicate"));
		impRoi=IJ.getImage();
		return impRoi;
	def registerIm(imp):
		IJ.run(imp,"StackReg", "transformation=[Translation]");
	

	#denoise and register the entire image
	imp = IJ.getImage();
	imName = imp.title;
	imDir = IJ.getDirectory("image");#TODO: check if this returns "None"
	IJ.run(imp,"PureDenoise ...", "parameters='3 4' estimation='Auto Individual' ");#This ives same results as manual run
	imp2 = IJ.getImage();
	IJ.run(imp2,"StackReg", "transformation=[Rigid Body]");
	imName2 = imName.replace(".tif","") +"_denoise_reg.tif";
	imp2.title=imName2;
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
		return;
	else:
		for ii in range(0,n):
			roiName = imName2.replace(".tif","") +"_ring"+str(ii+1)+".tif";
			impRoi=cropRoi(imp2,ii,roiName);
			registerIm(impRoi);
			#save roi
			imPath = os.path.join(analysisDir,roiName);
			IJ.saveAsTiff(impRoi,imPath);


			
preprocessRingFOV();