# About

This project uses OpenAI and Anthropic APIs to generate engaging conversations between two AI characters and converts them into audio podcasts using OpenAI's Text-to-Speech API.

## Features

- Generate natural conversations between two characters (currently a Painter and a Musician)
- Convert conversations to audio using OpenAI's TTS API
- Support for different voice options
- Save conversations as text files
- Combine multiple audio segments into a single podcast file

## Setup

1. Clone this repository
2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=sk-ant-xxxx
```

## Usage

### Generate a Conversation

Run the conversation script to generate a dialogue between the characters:

```bash
python conversation.py
```

This will:
- Generate a conversation between a Painter and a Musician
- Save the conversation to a text file (e.g., `conversation_YYYYMMDD_HHMMSS.txt`)
- Display the conversation and associated costs

### Convert Conversation to Audio

Convert a conversation text file to audio using:

```bash
python tts.py [conversation_file.txt] --speaker1 [voice1] --speaker2 [voice2]
```

Options:
- `[conversation_file.txt]`: Path to the conversation text file
- `--speaker1`: Voice for the Painter (default: alloy)
- `--speaker2`: Voice for the Musician (default: nova)

Available voices:
- Female voices: alloy, nova, shimmer
- Male voices: echo, fable, onyx

Example:
```bash
python tts.py conversation_20241216_192503.txt --speaker1 shimmer --speaker2 echo
```

The script will:
1. Generate individual audio clips for each dialogue line
2. Combine them into a single MP3 file
3. Save the final audio in the `audio` directory

## Project Structure

- `conversation.py`: Script to generate conversations using Claude and GPT
- `tts.py`: Script to convert text conversations to audio
- `requirements.txt`: Project dependencies
- `audio/`: Directory containing generated audio files
- `text/`: Directory containing saved conversation texts

## Jupyter Notebooks (Legacy)
- `01-openant-conversation.ipynb`: Original notebook for conversation generation
- `02-tts.ipynb`: Original notebook for text-to-speech conversion

## Notes

- Conversations are automatically saved with timestamps
- Audio files are saved in MP3 format
- The script will display API costs for conversation generation
- Make sure you have sufficient API credits for both conversation generation and audio conversion