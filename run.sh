#!/bin/bash
mkdir output
python3 d.py &
python3 e.py &
python3 f.py &
cd output
python3 -m http.server