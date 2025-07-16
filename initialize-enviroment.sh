#/bin/bash

# This script sets up your TCB-Drone project for TensorFlow development. 
# This script is written for Linux and assumes that you already have the 
# python3-venv package installed. 
# If the package is not installed, you may install it with the command 
# sudo apt install python3-venv 

# This script should be run just once, after the repo has been cloned and 
# before any python scripts are run. 

# Get tensorflow (CPU Version) 
python3 -m venv tensorflow 
source tensorflow/bin/activate 
pip install --upgrade pip 
pip install --upgrade tensorflow 

# Verify installation 
IS_INSTALLED=$(python -c "import tensorflow as tf; print(tf.__version__)"  | grep -Po "[0-9]+\.[0-9]+\.[0-9]+"  | wc -l)

if [[ $IS_INSTALLED -gt 0 ]] then
    echo "Installation Successful"
else
    echo "Installation unsuccessful"
    exit 1
fi

# Get and unpack the training data 
#wget 
printf "Download training data at: https://mega.nz/file/nxxWFT6Y#rBb-YZ8G2Q8OAEPg9swbxAAWKfhjdtvx2pC4IlthqkU\n" 

exit 0
