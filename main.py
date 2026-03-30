from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

def text_to_speech(input_text):
    audio = b"".join(elevenlabs.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # "George" - browse voices at elevenlabs.io/app/voice-library
        model_id="eleven_v3",
        output_format="mp3_44100_128",
    ))
    return audio

def speech_to_text(input_audio):
    text = elevenlabs.speech_to_text.convert(
        file=input_audio,
        model_id="scribe_v1",
    )
    return text

if __name__ == "__main__":
    print("Hello from elevenlabs-learning!")
    elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    initial_text="This is Rajesh Kamireddy, Working as a DevOps Engineer and learning how to use the ElevenLabs API for text-to-speech conversion."
    audio = text_to_speech(initial_text)
    play(audio)
    converted_text = speech_to_text(audio)
    print(converted_text.text)