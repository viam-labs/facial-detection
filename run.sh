#!/bin/bash
cd `dirname $0`
OS=$(uname)

if [ -f .installed ]
  then
    source .venv/bin/activate
  else
    if ! command -v uv 2>&1 >/dev/null; then
        pip install uv --break-system-packages
    fi
    uv venv --python 3.12
    source .venv/bin/activate
    if [[ $OS == "Linux" ]]; then
      uv pip install -U -r requirements-linux.txt
    else
      uv pip install -U -r requirements.txt
    fi
    if [ $? -eq 0 ]
      then
        touch .installed
    fi

    # viam-sdk and the required version of tensorflow are incompatible, so we hack this by installing
    # viam-sdk afterwards
    uv pip install viam-sdk==0.31.0

    if [[ $OS == "Linux" ]]; then
      echo "Running on Linux"
      echo "Updating and installing dependencies"
      sudo apt update && sudo apt upgrade -y
      sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6 -y
    fi
fi

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 -m src $@
