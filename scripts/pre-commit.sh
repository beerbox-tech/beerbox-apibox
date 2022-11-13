#!/bin/bash
EXIT=0

# run black checks
echo -n "format files with black .............. $(tput setaf 16)$(tput setab 6) ongoing $(tput sgr0) "
poetry run black --check src/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "\rformat files with black .............. $(tput setaf 16)$(tput setab 2) success $(tput sgr0) "
else
    poetry run black --check src/ > /dev/null 2>&1
    echo -e "\rformat files with black .............. $(tput setaf 16)$(tput setab 1) failure $(tput sgr0) "
    EXIT=1
fi

# run pylint checks
echo -n "lint files with pylint ............... $(tput setaf 16)$(tput setab 6) ongoing $(tput sgr0) "
poetry run pylint src/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "\rlint files with pylint ............... $(tput setaf 16)$(tput setab 2) success $(tput sgr0) "
else
    echo -e "\rlint files with pylint ............... $(tput setaf 16)$(tput setab 1) failure $(tput sgr0) "
    EXIT=1
fi

exit $EXIT
