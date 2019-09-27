#!/bin/bash
echo "Starting script."

cd ~/hilics
export DISPLAY=:0
chmod +x ./main.py
./main.py