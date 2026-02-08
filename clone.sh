#!/usr/bin/env bash
set -e

REF_AUDIO="$1"

if [[ -z "$REF_AUDIO" ]]; then
  echo "Usage: $0 <reference_voice.mp3>"
  exit 1
fi

python cloneVoice.py "$REF_AUDIO"

VOICE_PROMPT=$(cat voice_clone_prompt_path.txt)

python generateWazeWavs.py "$VOICE_PROMPT"
