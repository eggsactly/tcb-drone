#/bin/bash

# This script sets up your TCB-Drone project for TensorFlow development. 
# This script is written for Linux and assumes that you already have the 
# python3-venv package installed. 
# If the package is not installed, you may install it with the command 
# sudo apt install python3-venv 

# This script should be run just once, after the repo has been cloned and 
# before any python scripts are run. 

# Verify installation 
IS_INSTALLED=0
if [ -f tensorflow/bin/activate  ]; then
    source tensorflow/bin/activate
    IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)
fi

# If not already installed, get tensor flow 
if [[ $IS_INSTALLED -eq 0 ]] then
    # Get tensorflow (CPU Version) 
    python3 -m venv tensorflow 
    source tensorflow/bin/activate 
    pip install --upgrade pip 
    pip install --upgrade tensorflow 
    pip install opencv-python
    pip install pyyaml h5py  # Required to save models in HDF5 format
    
    # Verify installation 
    IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)

    if [[ $IS_INSTALLED -gt 0 ]] then
        echo "Installation Successful"
    else
        echo "Installation unsuccessful"
        exit 1
    fi
fi

wget https://tcb-drone.sfo3.digitaloceanspaces.com/Labels-20250715T043403Z-1-001.zip

unzip Labels-20250715T043403Z-1-001.zip


