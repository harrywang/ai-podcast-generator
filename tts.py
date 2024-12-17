import os
import sys
import argparse
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Available voices
# female: alloy, nova, shimmer | male: echo, fable, onyx
FEMALE_VOICES = ["alloy", "nova", "shimmer"]
MALE_VOICES = ["echo", "fable", "onyx"]

def speak(text, voice, temp_dir):
    """Generate speech from text and save to temporary file"""
    try:
        temp_file = os.path.join(temp_dir, f"{voice}_{hash(text)}.mp3")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(temp_file)
        return temp_file
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        return None

def process_conversation(filename, speaker1="alloy", speaker2="nova"):
    """Process conversation from file and generate combined audio"""
    try:
        # Read the conversation file
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Process each line
        current_speaker = None
        current_text = ""
        conversations = []
        
        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                if current_speaker and current_text:
                    conversations.append((current_speaker, current_text.strip()))
                    current_text = ""
                continue
                
            if line.startswith("Painter:"):
                if current_speaker and current_text:
                    conversations.append((current_speaker, current_text.strip()))
                current_speaker = "Painter"
                current_text = line[8:]  # Remove "Painter: "
            elif line.startswith("Musician:"):
                if current_speaker and current_text:
                    conversations.append((current_speaker, current_text.strip()))
                current_speaker = "Musician"
                current_text = line[10:]  # Remove "Musician: "
            else:
                current_text += " " + line

        # Add the last conversation if exists
        if current_speaker and current_text:
            conversations.append((current_speaker, current_text.strip()))

        # Create temporary directory for individual clips
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate audio clips
            print(f"\nGenerating audio...")
            audio_files = []
            for i, (speaker, text) in enumerate(conversations, 1):
                voice = speaker1 if speaker == "Painter" else speaker2
                print(f"Generating audio {i}/{len(conversations)} for {speaker}...")
                temp_file = speak(text, voice, temp_dir)
                if temp_file:
                    audio_files.append(temp_file)
                else:
                    print(f"Failed to create audio for segment {i}")

            if not audio_files:
                print("No audio clips were generated successfully.")
                return

            # Combine all clips
            print("\nCombining audio clips...")
            os.makedirs("./audio", exist_ok=True)
            
            # Create combined audio
            combined = AudioSegment.empty()
            for audio_file in audio_files:
                segment = AudioSegment.from_mp3(audio_file)
                combined += segment
            
            # Export final audio
            output_file = f"./audio/{os.path.splitext(os.path.basename(filename))[0]}.mp3"
            combined.export(output_file, format="mp3")

            print(f"\nAudio generation complete! Combined file saved as: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Convert conversation text to speech')
    parser.add_argument('filename', help='Input text file containing the conversation')
    parser.add_argument('--speaker1', default='alloy', choices=FEMALE_VOICES + MALE_VOICES,
                      help='Voice for the Painter (default: alloy)')
    parser.add_argument('--speaker2', default='nova', choices=FEMALE_VOICES + MALE_VOICES,
                      help='Voice for the Musician (default: nova)')
    
    args = parser.parse_args()
    
    print(f"\nProcessing conversation from: {args.filename}")
    print(f"Using voices: Painter={args.speaker1}, Musician={args.speaker2}")
    
    process_conversation(args.filename, args.speaker1, args.speaker2)

if __name__ == "__main__":
    main()
