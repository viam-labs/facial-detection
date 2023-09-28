#!/bin/bash
cd `dirname $0`

if [ -z "$IN_APPIMAGE" ] ; then
    pip install --upgrade -r requirements.txt
fi

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 -m src $@
