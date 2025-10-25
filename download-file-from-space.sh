#!/usr/bin/bash

URL_PREFIX="https://tcb-drone.sfo3.digitaloceanspaces.com/"
FORCE=0
USER_RESPONSE='y'

if [ $# -lt 1 ] || [ "$1" == "-f" ]
then 
    >&2 echo "${0}: Error: No file specified. Please provide name of file to download."
    exit 1
fi

# Check for presense of force flag 
if [ $# -ge 2 ] && [ "$2" == "-f" ] 
then
    FORCE=1
fi

# If the file exists and the force flag is not set, ask the user if they want to continue download 
if [ -f $1 ] && [ ${FORCE} -eq 0 ] 
then
   >&2 printf "${0}: Query: File exists, continue? (y/N): "
   read USER_RESPONSE
fi

if [ ! "$USER_RESPONSE" == "y" ]; then
    >&2 echo "${0}: Info: aborting download: ${1}" 
    exit 0
fi

wget ${URL_PREFIX}${1} 

ERROR=$?

if [ ${ERROR} -ne 0 ]; then 
    >&2 echo "${0}: Error: Could not download file: " `perror ${ERROR}`
    exit 1
fi

>&2 echo "${0}: Info: download successful: ${1}" 

exit 0

