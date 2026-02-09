# Audio Parser

This repository contains Python functions/modules to
- Download YouTube videos as mp4
- Convert mp4 to wav audio files
- Transcribe audio files with fast-whisper-small

## Setup

### Pre-requisites
1. Create a local untracked folder named `models` in the root of this repository.
2. Move the downloaded hugging face model: `faster-whisper-small` to the `models` folder

### Steps
1. Create venv in the root of this repository: `python -m venv venv` 
2. Activate the venv `source venv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Run `python main.py`

## Future Enhancements
1) Diarize with pyannote (speaker turns)
2) Extract explicit names from transcript
3) Align names to diarized speakers