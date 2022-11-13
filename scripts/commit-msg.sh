#!/bin/bash

MSG_FILE=$1
FILE_CONTENT="$(cat $MSG_FILE)"

REGEX="(fix|feat|refacto)\((core|users|contributions)\): [a-z]+"
ERROR_MSG="commit message format must match regex \"${REGEX}\""

if [[ $FILE_CONTENT =~ $REGEX ]]; then
    exit 0
else
    echo "bad commit \"$FILE_CONTENT\""
    echo $ERROR_MSG
    exit 1
fi
