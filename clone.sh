#!/usr/bin/env bash
set -e

REF_AUDIO="$1"

if [[ -z "$REF_AUDIO" ]]; then
  echo "Usage: $0 <reference_voice.mp3>"
  exit 1
fi

# Clear old WAV files
WAV_DIR="wavs"
if [[ -d "$WAV_DIR" ]]; then
  echo "Cleaning old WAV files in $WAV_DIR..."
  rm -rf "$WAV_DIR"/*
else
  mkdir -p "$WAV_DIR"
fi

python cloneVoice.py "$REF_AUDIO"
VOICE_PROMPT=$(cat voice_clone_prompt_path.txt)
python generateWazeWavs.py "$VOICE_PROMPT"

cd waze-voicepack-links
# Capture the main.py output
MAIN_OUTPUT=$(python mp3_upload/main.py)

# Extract the URL that starts with https://waze.com/ul?acvp=
WAZE_URL=$(echo "$MAIN_OUTPUT" | grep -o 'https://waze\.com/ul?acvp=[a-z0-9-]\+')

if [[ -n "$WAZE_URL" ]]; then
  echo "Waze URL: $WAZE_URL"
  echo "QR code:"
  # Display QR code in terminal
  qrencode -t ANSIUTF8 "$WAZE_URL"
else
  echo "No Waze URL found in the output."
fi
