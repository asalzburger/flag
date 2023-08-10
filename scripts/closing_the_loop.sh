export FLAG=$PWD
cd $ACTS/Examples/Scripts/Python
python3 flag_material_recording.py
cd $FLAG
python3 tools/material_mapping_inspector.py
cd $ACTS/Examples/Scripts/Python
python3 flag_material_mapping.py
cd $FLAG
