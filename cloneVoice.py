import argparse
import os
import torch
from qwen_tts import Qwen3TTSModel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_audio", help="Reference MP3 file for voice cloning")
    args = parser.parse_args()

    ref_audio = args.ref_audio
    base, _ = os.path.splitext(ref_audio)
    ref_text_path = base + ".txt"

    if not os.path.exists(ref_text_path):
        raise FileNotFoundError(f"Expected text file not found: {ref_text_path}")

    with open(ref_text_path, "r", encoding="utf-16") as f:
        ref_text = f.read().strip()

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        device_map="cuda:0",
        dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
    )

    prompt_items = model.create_voice_clone_prompt(
        ref_audio=ref_audio,
        ref_text=ref_text,
        x_vector_only_mode=False,
    )

    prompt_filename = base + "_voice_clone_prompt.pt"
    torch.save(prompt_items, prompt_filename)

    # Write the filename to a sidecar file for bash to read
    with open("voice_clone_prompt_path.txt", "w", encoding="utf-8") as f:
        f.write(prompt_filename)

if __name__ == "__main__":
    main()
