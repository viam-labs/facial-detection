#!/bin/bash
cd `dirname $0`

python3 -m pip install --user virtualenv
python3 -m venv viam-env
source viam-env/bin/activate
pip install --upgrade -r requirements.txt

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 -m src $@
