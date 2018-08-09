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

echo "Done! Components saved in ./test/output/remote/simulatorRun/components.pdf'";
