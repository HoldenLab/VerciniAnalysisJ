from ij import IJ;
from ij.plugin.frame import RoiManager
import os

rm = RoiManager.getInstance()
if (not rm) or rm.count==0:
    IJ.showMessage("Please draw or load ROIs");
else:
    n=rm.count;

    #Save ROIs in a folder
    imp = IJ.getImage();
    imName = imp.title;
    imDir = IJ.getDirectory("image");#TODO: check if this returns "None"
    k = imName.rfind(".tif");
    roiName = imName[:k] + ".roi.zip";
    rm.runCommand("save", os.path.join(imDir,roiName));

    #Delete ROI list
    rm.runCommand("Deselect");
    rm.runCommand("Delete");

