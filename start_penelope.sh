#!/bin/bash
# Start PENELOPE Service
cd "/media/juan/DATA2/projects/MAXIMUS AI"
export PYTHONPATH="/media/juan/DATA2/projects/MAXIMUS AI:$PYTHONPATH"
python3 services/penelope/main.py
