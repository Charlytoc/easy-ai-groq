#!/bin/bash
# Run npm watch-build
npm run watch-build &

# Run FastAPI application
python main.py
