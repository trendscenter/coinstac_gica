#!/bin/bash

docker build -t gica .;
coinstac-simulator;

cd test/remote/simulatorRun;
echo "Untarring data...";
tar -xzf template.tar.gz;
tar -xzf data.tar.gz;
cd ../../../matlab_dir;

matlab -nodesktop -nosplash -nodisplay -r "save_results;exit";

cd ..;

python montage_nii.py matlab_dir/components.nii test/remote/simulatorRun/ch.nii components.pdf 0

