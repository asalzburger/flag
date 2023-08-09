# Use a Python virtual environment
# source $VENV_DIR/bin/activate

python3 tools/silicon_cylinder_creator.py
# python3 tools/copy_silicon_cylinder_creator.py

# ACTS
export FLAG=$PWD
cd $ACTS/build/run
python3 material_recording.py
cd $FLAG
# The cylinder file should be linked to the directory where the ACTS Python
# file is.
# The file geant4_material_tracks.root created by material_recording.py needs
# to be linked to the directory data/geant4_root_files in order for the comparison
# further down to work.

# FLUKA
python3 tools/geant4_to_fluka.py data/cylinder_g4/silicon_cylinder.gdml
python3 tools/add_fluka_beg_and_end.py
cd data/cylinder_fluka
$MYFLUKA silicon_cylinder.inp
cd ../..
cd tools
gfortran readRay.f
cd ..
cd data/cylinder_fluka
./../../tools/a.out | tee fortran_output.txt
cd ../..
python3 tools/fortran_output_to_csv.py

# pyg4ometry
# export FLAG=$PWD
# cd $HOME/builds/acts/build/run
# python $HOME/builds/acts/build/run/material_recording.py
# cd $FLAG
python3 tools/geant4_fluka_comparison.py

