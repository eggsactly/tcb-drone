#/bin/bash

# This script sets up your TCB-Drone project for TensorFlow development. 
# This script is written for Linux and assumes that you already have the 
# python3-venv package installed. 
# If the package is not installed, you may install it with the command 
# sudo apt install python3-venv 

# This script should be run just once, after the repo has been cloned and 
# before any python scripts are run. 

# Name of the training set file, this may change PR to PR. 
TRAINING_SET=Labels-20250715T043403Z-1-001.zip

# Verify installation 
IS_INSTALLED=0
if [ -f tensorflow/bin/activate  ]; then
    source tensorflow/bin/activate
    IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)
fi

# If not already installed, get tensor flow 
if [[ $IS_INSTALLED -eq 0 ]] then
    # Delete the tensorflow folder if one exists and is not a verified install 
    rm -rf tensorflow/
    # Get tensorflow (CPU Version) 
    python3 -m venv tensorflow 
    source tensorflow/bin/activate 
    pip install --upgrade pip 
    pip install --upgrade tensorflow 
    pip install opencv-python
    pip install pyyaml h5py  # Required to save models in HDF5 format
    pip install botocore 
    pip install boto3
    
    # Verify installation 
    IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)

    if [[ $IS_INSTALLED -gt 0 ]] then
        echo "Installation Successful"
    else
        echo "Installation unsuccessful"
        exit 1
    fi
fi

# If the training set is not already downloaded, download it  
if [ ! -f ${TRAINING_SET} ]; then
    # Get the initial training set 
    wget https://tcb-drone.sfo3.digitaloceanspaces.com/${TRAINING_SET}

    # unzip the training set 
    unzip ${TRAINING_SET}
fi




