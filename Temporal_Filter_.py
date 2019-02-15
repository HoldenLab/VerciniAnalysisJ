#@ int	   (label="Time window half-width",description="t-window") tWindow
#@ boolean (label="Bleach correct imagage",description="beach-corredt") doBleachCorr
from ij import IJ;
import os
import fnmatch
from ij.plugin import ImageCalculator as ic

#tWindow=20;

IJ.run("Conversions...", " "); # ensure that IJ does not rescale when converting 32->16bit
imp=IJ.getImage();
#Warning - converts to 16 bit! 
IJ.run(imp, "16-bit", "");

if doBleachCorr:
    IJ.run(imp,"Bleach Correction", "correction=[Exponential Fit]");
    imp = IJ.getImage();

IJ.run(imp,"Trails", "time="+str(tWindow));
imp_tSmooth= IJ.getImage();

IC1 = ic();
imp_tFilt = IC1.run("Subtract create 32-bit stack",imp,imp_tSmooth);


imp_tFilt.show();
