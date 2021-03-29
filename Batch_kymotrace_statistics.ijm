#@ Float (label="Pixel size (nm)",description="pixSz") PIXSZ
#@ Float (label="Frame interval (s)",description="frTime") FRTIME


macro "Batch Kymo Trace Statistics" {
	//Select directory for analysis (images can be in subfolders)
	maindir = getDirectory("Choose the root Directory ");
	maindirName = File.getName(maindir);
	
	setBatchMode(true);
	
	//Create a list of tiff files in maindir
	String.resetBuffer;		//needed as the buffer is used to store the Tiff list as a string in ListTiffFiles
	TiffList = ListTiffFiles(maindir);
	
	// Empties ROI manager
	nROI = roiManager("count");
	if (nROI!=0) {
		roiManager("Deselect");
		roiManager("Delete");
	}
	
	// Define threshold speed for static
	staticThreshold = 0.02;
	
	// Prepare the Results table
	TableName = maindirName + "_tracks_global.csv";
	title1 = "" + maindirName + "_results";
	title2 = "[" + title1 + "]";
	f = title2;
	if (isOpen(title1))
		print(f, "\\Clear");
	else
	run("New... ", "name=" + title2 + " type=Table");
	Headings = "\\Headings:n\tROI#\tImage&ROI_Name\tDisplacement (nm)\tTime (s)\tVelocity (nm/s)\tThetaDeg\tThetaRad";
	print(f, Headings);
	roiNumber = 0;
	resultsLine = 0;
		
	// Measures all ROIs for all images in the list of Tiff that have a ROI set
	Nimage = 0;
	for (i=0; i<TiffList.length; i++) {
		ImageFullPath = TiffList[i];
		ImagePath = File.getParent(ImageFullPath);
		ImageName = File.getName(ImageFullPath);
		ImageNameCropped = substring(ImageName, 0, lastIndexOf(ImageName, ".tif"));
		ROIpath = ImagePath + File.separator + ImageNameCropped + ".roi.zip";

		// Open image i
		open(ImageFullPath);
		sourceID = getImageID();
		selectImage(sourceID);
		// Open ROI file for image i
		if (File.exists(ROIpath)) {
			roiManager("Open", ROIpath);
			
			
			// Get scale and ROI number
			// ImageName = getTitle();
			//getVoxelSize(pX, pY, pZ, pUnit);
			nROI = roiManager("count");
			
								
			// Measure ROIs for image i
			for (r = 0; r < nROI; r++) {
				// Select ROI
				roiManager("select", r);

				// Get ROI name, properties and number
				roiTitle = getInfo("selection.name");
				ROIname = ImageNameCropped + "_" + roiTitle;
				roiNumber = r + 1;
						
				// get ROI coordinates
				Roi.getCoordinates(xpoints, ypoints);
				L = xpoints.length;
				// Array.print(xpoints);
				// Array.print(ypoints);
				
				// Scaled coordinates
				//xS = newArray(L);
				//yS = newArray(L);
				//for (p = 0; p < L; p++) {
					//xS[p] = xpoints[p] * PIXSZ;
					//yS[p] = ypoints[p] * FRTIME;
				//}
				
				// Coordinates differences
				dx = newArray(L);
				dy = newArray(L);
				// Using index=0 to store global difference between extremities
				dx[0] = xpoints[L-1] - xpoints[0];
				dy[0] = ypoints[L-1] - ypoints[0];
				// 1 to L for single-step differences
				for (p = 1; p < L; p++) {
					dx[p] = xpoints[p] - xpoints[p - 1];
					dy[p] = ypoints[p] - ypoints[p - 1];
				}
				
				// Scaled differences (0 is global, 1-L for each step)
				dxS = newArray(L);
				dyS = newArray(L);
				for (p = 0; p < L; p++) {
					dxS[p] = dx[p] * PIXSZ;
					dyS[p] = dy[p] * FRTIME;
				}
				
				// Speeds (O is global, 1-L for each step)
				V = newArray(L);
				for (p = 0; p < L; p++) {
					V[p] = (dxS[p]) / (dyS[p]);
				}
				
				// Angle
				ThetaDeg = newArray(L);
				ThetaRad = newArray(L);
				// Using index=0 to store global angle
				ThetaDeg[0] = (180/PI)*atan2(dx[0], dy[0]);
				ThetaRad[0] = atan2(dx[0], dy[0]);
				
				// 1 to L for single-step differences
				for (p = 1; p < L; p++) {
					ThetaDeg[p] = (180/PI)*atan2(dx[p], dy[p]);
					ThetaRad[p] = atan2(dx[p], dy[p]);
				}
				
				// Category (anterograde = +1, retrograde = -1, static = 0);
				Cat = newArray(L);
				for (p = 0; p < L; p++) {
					if (V[p] > staticThreshold) Cat[p] = 1;
					else if (V[p] < -staticThreshold) Cat[p] = -1;
					else Cat[p] = 0;		
				}
				
				for (k = 0; k < 1; k++) {
					resultsLine++;
					// Build the Results table line
					ResultsLine = d2s(resultsLine, 0) + "\t" + roiNumber + "\t" + ROIname + "\t" + dxS[k] + "\t" + dyS[k] + "\t" + V[k] + "\t" + ThetaDeg[k] + "\t" + ThetaRad[k] ;
					print(f, ResultsLine);
				}
			}
			
			roiManager("Deselect");
			roiManager("Delete");
			print(ImageName);
			Nimage = Nimage + 1;
		}
		selectImage(sourceID);
		close();
	}
		
	print("N(image) = " + Nimage);
	print("N(track) = " + resultsLine);
	print("");

	selectWindow(title1);
	saveAs("Text", maindir + File.separator + TableName);
	// run("Close");

	setBatchMode(false);
	
}


function ListTiffFiles(dir) {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		if (endsWith(list[i], "tif") || endsWith(list[i], "tiff")) {
			String.append(dir + list[i] + "\t");
			}
	}
	str = String.buffer;
	list2 = split(str, "\t");
	return list2;
}
