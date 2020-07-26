#!/bin/bash

pip install "$@" torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
pip install "$@" -r requirements.txt
pip install "$@" -r PhotoInpainting/requirements.txt
