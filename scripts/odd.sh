# Move the file you want to display into the directory with the template files
# geoPluginRun -input $HOME/builds/acts/thirdparty/OpenDataDetector/xml/OpenDataDetector.xml -interactive -plugin DD4hep_GeometryDisplay -level 8
# geoPluginRun -input $HOME/builds/acts/thirdparty/OpenDataDetector/xml/ExperimentalOpenDataDetector.xml -interactive -plugin DD4hep_GeometryDisplay -level 8

# export FLAG=$PWD
# cd $ACTS/Examples/Scripts/Python
# python3 flag_geometry.py
# geoPluginRun -input $HOME/builds/acts/thirdparty/OpenDataDetector/xml/OpenDataDetector.xml -interactive -plugin DD4hep_GeometryDisplay -level 1
# cd $FLAG

# export FLAG=$PWD
# cd $ACTS/Examples/Scripts/Python
# python3 flag_geometry.py
# geoPluginRun -input $HOME/builds/acts/thirdparty/OpenDataDetector/xml/OpenDataDetector.xml -interactive -plugin DD4hep_GeometryDisplay -level 8 << EOF
# gGeoManager->Export("$FLAG/data/open_data_detector/ODD_Pixel_l0.gdml")
# EOF
# python3 flag_material_recording.py
# cd $FLAG

export FLAG=$PWD
cd $ACTS/Examples/Scripts/Python
python3 flag_tracking_geometry.py
python3 flag_dd4hep_geometry.py
python3 flag_material_recording.py
python3 flag_material_mapping.py
cd $FLAG