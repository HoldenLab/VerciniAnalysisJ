macro "Batch measure linear kymograph" {
    ImageName = getTitle();
    RootDir= getDirectory("image");
    KymoDir = RootDir + "Indiv_kymographs" + File.separator;
    // Find a way not to overwrite folders
    //if (!File.exists(RingDir)) {
    //	RingDir = RingDir + "-1" + File.separator;
    //}
    File.makeDirectory(KymoDir);

    id = getImageID();
    for (i=0 ; i<roiManager("count"); i++) {
            selectImage(id);
        roiManager("select", i);
        current = Roi.getName();
        fullpath = KymoDir + File.separator + current;
        run("Kymograph", "linewidth=3");
        saveAs("tiff", fullpath);
        close();
        }
}
