import argparse
import csv
import os
import subprocess
import torch
import transformers
transformers.logging.set_verbosity_error()
import soundfile as sf
from qwen_tts import Qwen3TTSModel

BATCH_SIZE = 4
WAV_DIR = "wavs"
MP3_ROOT_DIR = "waze-voicepack-links/mp3_upload/input_packs"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("voice_clone_prompt", help="Path to .pt voice clone prompt")
    args = parser.parse_args()

    # Extract <NAME> from <NAME>_voice_clone_prompt.pt
    prompt_basename = os.path.basename(args.voice_clone_prompt)
    if not prompt_basename.endswith("_voice_clone_prompt.pt"):
        raise ValueError("Expected prompt filename to end with '_voice_clone_prompt.pt'")
    name_prefix = prompt_basename.replace("_voice_clone_prompt.pt", "")

    # Create output subfolder for this voice pack
    MP3_DIR = os.path.join(MP3_ROOT_DIR, name_prefix)
    os.makedirs(WAV_DIR, exist_ok=True)
    os.makedirs(MP3_DIR, exist_ok=True)

    print(f"Using MP3 output directory: {MP3_DIR}")

    # Load model and voice prompt
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        device_map="cuda:0",
        dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
    )

    prompt_items = torch.load(args.voice_clone_prompt, weights_only=False)

    texts = []
    output_files = []

    with open("prompts.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].lower() == "text":
                continue

            text, output_file = row
            texts.append(text)
            output_files.append(os.path.join(WAV_DIR, output_file))

    # Generate WAVs in batches
    for start in range(0, len(texts), BATCH_SIZE):
        end = start + BATCH_SIZE

        batch_texts = texts[start:end]
        batch_files = output_files[start:end]
        batch_languages = ["English"] * len(batch_texts)

        print(f"Generating batch {start}-{end - 1}")

        with torch.no_grad():
            wavs, sr = model.generate_voice_clone(
                text=batch_texts,
                language=batch_languages,
                voice_clone_prompt=prompt_items,
            )

        for wav, filename in zip(wavs, batch_files):
            sf.write(filename, wav, sr)

        del wavs
        torch.cuda.empty_cache()

    # Convert WAVs to MP3s inside the <NAME> folder
    for filename in os.listdir(WAV_DIR):
        if not filename.lower().endswith(".wav"):
            continue

        wav_path = os.path.join(WAV_DIR, filename)
        mp3_path = os.path.join(MP3_DIR, os.path.splitext(filename)[0] + ".mp3")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", wav_path,
                "-codec:a", "libmp3lame",
                "-qscale:a", "2",
                mp3_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

if __name__ == "__main__":
    main()
