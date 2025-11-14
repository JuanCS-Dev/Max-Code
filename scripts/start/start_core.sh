#!/bin/bash
# Start MAXIMUS Core Service
cd "/media/juan/DATA2/projects/MAXIMUS AI"
export PYTHONPATH="/media/juan/DATA2/projects/MAXIMUS AI:$PYTHONPATH"
python3 services/core/main.py
