# FLUKA
python3 tools/silicon_cylinder_creator.py
python3 tools/geant4_to_fluka.py data/cylinder_pyg4ometry/silicon_cylinder.gdml
python3 tools/add_fluka_beg_and_end.py
cd data/cylinder_fluka
$MYFLUKA silicon_cylinder.inp
cd ../..
cd tools
gfortran readRay.f
cd ..
cd data/cylinder_fluka
./../../tools/a.out
# fort.10 | ./../../tools/a.out
cd ../..

# pyg4ometry
# python $HOME/builds/acts/build/run/material_recording.py
python3 tools/geant4_fluka_comparison.py

