run("Action Bar","/scripts/Plugins/VerciniAnalysisJ/Start_Vercini_ActionBar.ijm")
exit();

<line>
<button> 1 line 1
label=Start ROI manager
icon=noicon
arg=<macro>
run("Start ROI manager");
</macro>
</line>
<line>
<button> 2 line 1
label=Draw 60x60 ROI
icon=noicon
arg=<macro>
run("Draw 60x60 ROI");
</macro>
</line>
<line>
<button> 3 line 1
label=Save ROIs
icon=noicon
arg=<macro>
run("Save ROI ");;
</macro>
</line>
<line>
<button> 4 line 1
label=Batch denoise+register+crop
icon=noicon
arg=<macro>
run("Batch denoise register crop");
</macro>
</line>
<line>
<button> 5 line 1
label=Batch denoise+register
icon=noicon
arg=<macro>
run("Batch denoise register");
</macro>
</line>
<line>
<button> 6 line 1
label=Batch denoise
icon=noicon
arg=<macro>
run("Batch denoise");
</macro>
</line>
<line>
<button> 7 line 1
label=Batch crop
icon=noicon
arg=<macro>
run("Batch crop");
</macro>
</line>
<line>
<button> 8 line 1
label=Remove last row
icon=noicon
arg=<macro>
run("Remove last row");
</macro>
</line>
<line>
<button> 9 line 1
label=Ridge Filter
icon=noicon
arg=<macro>
run("Ridge Filter");
</macro>
</line>
<line>
<button> 10 line 1
label=Batch kymotrace statistics
icon=noicon
arg=<macro>
run("Batch kymotrace statistics");
</macro>
</line>

