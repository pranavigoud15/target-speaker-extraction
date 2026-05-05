# Target Speaker Extraction

This project > Extracts a target speaker from noisy multi-speaker audio using deep learning (PyTorch)

## Features
- Extracts specific speaker from noisy audio
- Uses pretrained models for audio processing
- Supports multiple audio inputs

## Tech Stack
- Python
- PyTorch
- Audio Processing

## How to Run

pip install -r requirements.txt  
python app.py

## Demo

### Input Audio
[Click to play](demo/input.wav)

### Output Audio (Extracted Speaker)
[Click to play](demo/output.wav)

## What happens here?

- Input: Mixed audio containing multiple speakers  
- Output: Clean audio of the target speaker extracted using deep learning model

- ## Results

- Successfully separates target voice from overlapping speech
- Works on short audio samples (~5–10 sec)

## Note
Model files (.pt) and pretrained models are excluded due to large size.
