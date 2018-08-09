#!/bin/bash

cd test/remote/simulatorRun;
echo "Untarring data...";
tar -xzf template.tar.gz;
tar -xzf data.tar.gz;

cd ../../..;
echo "Buildingg docker file...";
docker build -t gica .;
echo "Running Simulator...";
coinstac-simulator;

cd matlab_dir;
echo "Displaying results...";
matlab -nodesktop -nosplash -nodisplay -r "save_results;exit";

cd ..;

python montage_nii.py matlab_dir/components.nii test/remote/simulatorRun/ch.nii components.pdf 0

