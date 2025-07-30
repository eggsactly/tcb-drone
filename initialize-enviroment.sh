#/bin/bash

# This script sets up your TCB-Drone project for TensorFlow development. 
# This script is written for Linux and assumes that you already have the 
# python3-venv package installed. 
# If the package is not installed, you may install it with the command 
# sudo apt install python3-venv 

# This script should be run just once, after the repo has been cloned and 
# before any python scripts are run. 

# Run with GPU arg to set up tensorflow with cuda. To download cuda toolkit, reference:
# https://docs.nvidia.com/cuda/cuda-installation-guide-linux

# Verify installation 
IS_INSTALLED=0

if [[ $1 == "GPU" ]]; then
    tf_ver="tensorflow[and-cuda]"
    check_tf_installed () {
        # Check that a GPU device is listed
        GPU_DEVICE=$(python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))" | grep -Po "\[PhysicalDevice\(.*\)\]")
        echo "GPU Device Found: ${GPU_DEVICE}"
        if [[ -n "{GPU_DEVICE}" ]]; then
            IS_INSTALLED=1
        fi
    }
else
    tf_ver="tensorflow"
    check_tf_installed () {
       # Verify installation 
        IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)
    }
fi

if [ -f tensorflow/bin/activate  ]; then
    source tensorflow/bin/activate
    check_tf_installed
fi

# If not already installed, get tensor flow 
if [[ $IS_INSTALLED -eq 0 ]] then
    # Get tensorflow (CPU Version) 
    python3 -m venv tensorflow 
    source tensorflow/bin/activate 
    pip install --upgrade pip 
    pip install --upgrade ${tf_ver}
    pip install opencv-python
    pip install pyyaml h5py  # Required to save models in HDF5 format
    
    # Verify installation 
    check_tf_installed

    if [[ $IS_INSTALLED -gt 0 ]] then
        echo "Installation Successful"
    else
        echo "Installation unsuccessful"
        exit 1
    fi
fi

# Ask the user if they want to be directed to the training set 
HAS_ZENITY=$(which zenity | wc -l)

if [[ $HAS_ZENITY -gt 0 ]] then
    zenity --question --text="Can we open a web browser to point you to the training set?"
    USER_RESPONSE=$?
else
    printf "Can we open a web browser to point you to the training set? (y/N)"
    read USER_RESPONSE 
    if [[ $USER_RESPONSE == "y" ]] then
        USER_RESPONSE=0
    else
        USER_RESPONSE=1
    fi
fi

# Get and unpack the training data 
#wget 
if [[ $USER_RESPONSE -eq 0 ]] then
    xdg-open https://mega.nz/file/nxxWFT6Y#rBb-YZ8G2Q8OAEPg9swbxAAWKfhjdtvx2pC4IlthqkU
else
    printf "Download training data at: https://mega.nz/file/nxxWFT6Y#rBb-YZ8G2Q8OAEPg9swbxAAWKfhjdtvx2pC4IlthqkU\n" 
fi
exit 0

