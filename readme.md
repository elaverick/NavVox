 NavVox

NavVox 🚗🎙️
============

**NavVox** is a tool for generating custom Waze voice packs using **Qwen3-TTS**. It takes a clean voice sample, clones the speaker’s voice, and generates MP3 navigation prompts ready for use in Waze.

This project uses an external conversion tool (included as a git submodule) to ensure compatibility with Waze’s voice pack format.

* * *

✨ Features
----------

*   Clone a voice from a single high-quality MP3 sample
*   Generate Waze-compatible MP3 voice prompts
*   Uses **Qwen3-TTS** for high-quality speech synthesis
*   Modular design with external tools managed via git submodules

* * *

🧰 Prerequisites
----------------

### Required

*   Python (3.9+ recommended)
*   FFmpeg
*   Qwen3-TTS

### Recommended

*   Python virtual environment (`venv`, `virtualenv`, or similar)

* * *

🗂️ Input Requirements
----------------------

To clone a voice, you must provide:

1.  **A clean MP3 file** of the voice you want to clone
    *   Minimal background noise
    *   Clear, natural speech
    *   Preferably 10–30 seconds or longer
2.  **A matching TXT transcription file**
    *   Must have the **same filename** as the MP3
    *   Must transcribe **exactly** what is spoken in the MP3

### Example

    voice_sample.mp3
    voice_sample.txt
    

* * *

📥 Cloning the Repository
-------------------------

This project uses a **git submodule**, so make sure to clone it correctly.

### Option 1: Clone with submodules (recommended)

    git clone --recurse-submodules https://github.com/YOUR_USERNAME/NavVox.git
    

### Option 2: Clone first, then init submodules

    git clone https://github.com/YOUR_USERNAME/NavVox.git
    cd NavVox
    git submodule update --init --recursive
    

* * *

🐍 Python Setup
---------------

Create and activate a virtual environment (recommended):

    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    # or
    venv\Scripts\activate      # Windows
    

Install Python dependencies (if applicable):

    pip install -r requirements.txt
    

_Note: If `requirements.txt` does not exist yet, install dependencies according to your Qwen3-TTS setup._

* * *

🎙️ Preparing Your Voice Sample
-------------------------------

1.  Place your `.mp3` and `.txt` files in the appropriate input directory
2.  Ensure:
    *   Filenames match exactly
    *   Transcription text is accurate
    *   Audio is clean and uncompressed if possible

* * *

▶️ Running the Tool
-------------------

To clone a voice and generate the output:

    ./clone.sh <MP3_FILENAME>
    

### Example

    ./clone.sh voice_sample.mp3
    

This script will:

*   Use the MP3 + TXT pair to clone the voice
*   Generate MP3 navigation prompts
*   Convert them into a Waze-compatible voice pack format

* * *

📦 Output
---------

*   Generated MP3 files suitable for Waze
*   Output structure depends on the conversion tool used via the submodule

Refer to the Waze voice pack documentation or the included submodule README for details on importing into Waze.

* * *

🔄 Updating the Submodule
-------------------------

    cd waze-voicepack-links
    git pull origin main
    cd ..
    git add waze-voicepack-links
    git commit -m "Update waze voicepack submodule"
    

* * *

⚠️ Notes & Tips
---------------

*   Voice quality matters — garbage in, garbage out
*   Make sure FFmpeg is available in your system PATH
*   This project is intended for personal and experimental use

* * *

📄 License
----------

Please check individual submodules for their respective licenses. NavVox itself is provided as-is.

* * *

🙌 Acknowledgements
-------------------

*   Qwen3-TTS for voice synthesis
*   pipeeeeees/waze-voicepack-links for Waze voice pack conversion tooling

Happy navigating — and enjoy hearing _your_ voice give directions! 🚗🗣️