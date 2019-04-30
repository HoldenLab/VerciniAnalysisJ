#@ Float(label="Smoothing scale (pix.)",value=2) smoothScale
run("FeatureJ Hessian", "smallest smoothing="+smoothScale);
run("Multiply...", "value=-1");
run("Min...", "value=0");
