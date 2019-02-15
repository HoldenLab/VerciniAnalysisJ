#@ File    (label = "Input directory", style = "directory") srcFile
#@ String  (label = "File filter") fileFilter
#@ boolean (label = "Search subdirectories") doRecursiveSearch
#@ double (label = "Pixel size (um)") pixelSizeUm
#@ double (label = "Exposure time (s)") expTime
#@ double (label = "Spot diameter") diameter
#@ double (label = "Quality threshold") threshold
#@ double (label = "Kalman initial search radius") initialSearchRadius #Kalman Initial search radius
#@ double (label = "Kalman max search radius") maxSearchRadius # Kalman max search radius
#@ int (label = "Max frame gap") frameGap
# Ignores directories named exclude


from ij import IJ;
import os
import fnmatch
import java.io.File as File
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.detection.LogDetectorFactory as LogDetectorFactory
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils
import fiji.plugin.trackmate.tracking.kalman.KalmanTrackerFactory as KalmanLAPTrackerFactory
import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML


def main():
    srcDir = srcFile.getAbsolutePath();
               
    for root, directories, filenames in os.walk(srcDir, topdown=True):
        if not doRecursiveSearch and root != srcDir:
            continue
        #Ignore any directories named "exclude" 
        directories[:] = [directory for directory in directories if directory != "exlude"];
        
        for filename in filenames:
            # Check for file name pattern
            if not fnmatch.fnmatch(filename, fileFilter):
                continue
            tifPath = os.path.join(root,filename);
            print "Processing file \""+filename+"\""
            processFile(tifPath);
    
def processFile(tifPath):
    #open the file
    imp = IJ.openImage(tifPath);
    imp.show();

    #manually set the scale to avoid imagej screw ups
    cal = imp.calibration;
    cal.pixelWidth=pixelSizeUm;
    cal.pixelHeight=pixelSizeUm;
    cal.pixelDepth=pixelSizeUm;
    cal.unit="um";
    imp.calibration=cal;
    imp.updateAndDraw;


    # Swap Z and T dimensions if T=1
    dims = imp.getDimensions() # default order: XYCZT
    if (dims[4] == 1):
        imp.setDimensions( dims[2],dims[4],dims[3] )
    dims = imp.getDimensions() # default order: XYCZT
         
    # Setup settings for TrackMate
    settings = Settings()
    settings.setFrom(imp)
    settings.dt = expTime
     
    settings.detectorFactory = LogDetectorFactory()
    settings.detectorSettings = settings.detectorFactory.getDefaultSettings()

    radius = diameter/2.0
    settings.detectorSettings['RADIUS'] = radius
    settings.detectorSettings['THRESHOLD'] = threshold
    settings.detectorSettings['DO_MEDIAN_FILTERING'] = True
         
    settings.trackerFactory = KalmanLAPTrackerFactory()
    settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
     
    #settings.trackerSettings['GAP_CLOSING_MAX_FRAME_GAP']  = frameGap 
    settings.trackerSettings['MAX_FRAME_GAP']  = frameGap 
    settings.trackerSettings['LINKING_MAX_DISTANCE']  = initialSearchRadius #Kalman Initial search radius
    settings.trackerSettings['KALMAN_SEARCH_RADIUS']  = maxSearchRadius #Kalman max search radius


    # Run TrackMate and store data into Model
    model = Model()
    trackmate = TrackMate(model, settings)
     
    trackmate.checkInput()
    trackmate.process()

    print "Number of spots: " + str( model.getSpots().getNSpots(True))
    print "Number of tracks: " +  str(model.getTrackModel().nTracks(True))

    imp.close()

    # Save tracks as XML
    xmlPath = tifPath.replace(".tif",".xml") 
 
    outFile = File(xmlPath)
    ExportTracksToXML.export(model, settings, outFile)

    # Save parameters to text file
    paramPath = tifPath.replace(".tif","_par.txt") 
    fh = open(paramPath,"w")
    fh.write("spotDetector\tLoG")
    fh.write("\n")
    fh.write("radius\t"+str(radius))
    fh.write("\n")
    fh.write("theshold\t"+str(threshold))
    fh.write("\n")
    fh.write("tracker\tLinearLAP")
    fh.write("\n")    
    fh.write("frameGap\t"+str(frameGap))
    fh.write("\n")    
    fh.write("initialSearchRadius\t"+str(initialSearchRadius))
    fh.write("\n")    
    fh.write("maxSearchRadius\t"+str(maxSearchRadius))
    fh.write("\n")    
    fh.close()    

main()


