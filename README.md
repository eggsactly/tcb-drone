# About
tcb-drone measures tree health from aerial photographs from drone flyovers of Tucson Clean and Beautiful planting locations. This project enables automated surveys of tree survival to provide data to improve neighborhood heat resilience.

## Technical
This git project implements neural networks and machine learning to identify trees and assess tree health. This project leverages TensorFlow to implement machine learning algorithms to assess tree health based on aerial photographs of trees.

# Setup
Once this repo is cloned, developers may setup their development enviroment by running
```
./initialize-enviroment.sh
```
which will install TensorFlow locally in the development sandbox.

If the developer wishes to employ a GPU to accelerate training runtimes, and is on a system that uses an nVidia GPU and has CUDA installed, the developer may setup their development enviroment by running: 
```
./initialize-enviroment.sh GPU
```

## Uploading new data
First create your `password.json` file in the following format
```
{
    "aws_access_key_id":"________________",
    "aws_secret_access_key": "_____________"
}
```

Second, upload a new file to the Digital Ocean spaces with the command 
`space-connect.py [path-to-file]`

# Project Progress and Tracking
A [Trello Board](https://trello.com/b/RLBbTfDf/tcb-drone-survey) is being used 
for project progress and task tracking. 

