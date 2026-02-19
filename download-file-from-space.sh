#!/usr/bin/bash

URL_PREFIX="https://tcb-drone.sfo3.digitaloceanspaces.com/"
FORCE=0
USER_RESPONSE='y'
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
HAS_PERROR=$(which perror | wc -l)
HAS_WGET=$(which wget | wc -l)
HAS_GREP=$(which grep | wc -l)
HAS_TAIL=$(which tail | wc -l)

if [ ${HAS_WGET} -eq 0 ]; then 
    >&2 printf "${0}: Error: wget is required, but not installed, please install wget.\n"
    exit 1
fi

if [ $# -lt 1 ] || [ "$1" == "-f" ]
then 
    >&2 printf "${0}: Error: No file specified. Please provide name of file to download.\n"
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

if [ ! "${USER_RESPONSE}" == "y" ]; then
    >&2 printf "${0}: Info: aborting download: ${1}\n" 
    exit 0
fi

# Attempt to download the file 
wget ${URL_PREFIX}${1} 

ERROR=$?

# If download was unsuccessful
# Server issued an error response. Exec format error.
if [ ${ERROR} -eq 8 ]; then 

    # Check if required applications are installed    
    if [ ${HAS_TAIL} -eq 0 ]; then 
        >&2 printf "${0}: Error: tail is required, please install tail.\n"
        exit 1
    fi
    
    if [ ${HAS_GREP} -eq 0 ]; then 
        >&2 printf "${0}: Error: grep is required, please install grep.\n"
        exit 1
    fi
    
    # See if name was a dir
    thestring=$1
    last_char=$(echo -n "$thestring" | tail -c 1)
    
    if [ ! "${last_char}" == "/" ]; then
        thestring="${thestring}/"
    fi
    
    numFilesInDir=$(${SCRIPT_DIR}/list-files-in-space.py -n | grep "${thestring}" | wc -l)

    if [ ${numFilesInDir} -gt 0 ]; then
        names=$(${SCRIPT_DIR}/list-files-in-space.py -n | grep "${thestring}")
        
        i=1;
        while read n; do 
          mkdir -p $(dirname ${n}) 
          if [ -f ${n} ] && [ ${FORCE} -eq 0 ] 
          then
             >&2 printf "${0}: Warning: ${n} exists, skipping. Use -f to overwrite\n"
             read USER_RESPONSE 
             if [ ! "${USER_RESPONSE}" == "y" ]; then
                 i=$(($i+1)); 
                 continue 
             fi
          fi
          wget ${URL_PREFIX}${1} -o ${n}
          i=$(($i+1)); 
        done <<< "$names"  
    else
        >&2 printf "${0}: Error: Could not find files in the directory.\n"
    fi
elif [ ${ERROR} -ne 0 ]; then 
    if [ ${HAS_PERROR} -gt 0 ]; then 
        >&2 printf "${0}: Error: Could not download file: %s\n" "`perror ${ERROR}`"
    else
        >&2 printf "${0}: Error: Could not download file, error code: %d\n" ${ERROR}
    fi
    exit 1
fi


>&2 printf "${0}: Info: download complete: ${1}\n" 

exit 0

