import subprocess
import platform
import os
from gtts import gTTS
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

def text_to_speech_with_gtts(input_text, output_filepath, play_audio=True):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    if play_audio:
        os_name = platform.system()
        try:
            if os_name == "Darwin":
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":
                subprocess.run(['start', '', output_filepath], shell=True)  # Use start command for MP3
            elif os_name == "Linux":
                subprocess.run(['mpg123', output_filepath])  # Use mpg123 for MP3 playback
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['start', '', output_filepath], shell=True)  # Use start command for MP3
        elif os_name == "Linux":
            subprocess.run(['mpg123', output_filepath])  # Use mpg123 for MP3 playback
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    audio_content = b''.join(audio)  # Collect all chunks from the generator
    with open(output_filepath, 'wb') as f:
        f.write(audio_content)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  
            subprocess.run(['start', '', output_filepath], shell=True)  # Use start command for MP3
        elif os_name == "Linux":  
            subprocess.run(['mpg123', output_filepath])  # Use mpg123 for MP3 playback
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

if __name__ == "__main__":
    text_to_speech_with_gtts(input_text="Hi this is Ai with Hassan, autoplay testing!", output_filepath="gtts_testing_autoplay.mp3")
    text_to_speech_with_elevenlabs(input_text="Hi this is Ai with Hassan!", output_filepath="elevenlabs_testing.mp3")
