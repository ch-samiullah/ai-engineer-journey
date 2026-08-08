# =============================================
# TARS — voice.py
# Speech Input + ElevenLabs Output
# =============================================

import speech_recognition as sr       # mic se sunna
import pygame                          # 🆕 audio play karne ke liye
import requests                        # ElevenLabs API call
import os
import io                              # 🆕 memory mein audio handle karna
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# 🆕 pygame mixer — audio playback ke liye
pygame.mixer.init()

# ----------------------------------------
# ElevenLabs Voice ID — TARS ki voice
# ----------------------------------------

# 🆕 Voice ID — ElevenLabs pe har voice ka unique ID hota hai
# "Adam" — deep professional male voice — TARS jaisi
VOICE_ID = "pNInz6obpgDQGcFmaJgB"

# ----------------------------------------
# FUNCTION 1 — TARS bolega ElevenLabs se
# ----------------------------------------

def speak(text):
    print(f"\nTARS: {text}")

    try:
        # ElevenLabs API call
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,    # API key header
            "Content-Type": "application/json"
        }

        body = {
            "text": text,
            "model_id": "eleven_monolingual_v1",  # 🆕 English model
            "voice_settings": {
                "stability": 0.5,        # 🆕 voice stability — 0 to 1
                "similarity_boost": 0.75  # 🆕 original voice se similarity
            }
        }

        # API se audio lao
        response = requests.post(url, json=body, headers=headers)

        if response.status_code == 200:
            # 🆕 io.BytesIO — audio bytes ko memory mein rakhna
            # file save nahi karte — directly play karte hain
            audio_data = io.BytesIO(response.content)

            # 🆕 pygame se play karo
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()

            # 🆕 play hone tak wait karo
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print(f"ElevenLabs Error: {response.status_code}")

    except Exception as e:
        print(f"Voice error: {e}")

# ----------------------------------------
# FUNCTION 2 — Mic se suno
# ----------------------------------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Listening...")

        # 🆕 noise adjustment — background noise filter karo
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        # 🆕 dynamic threshold — automatically noise level set karta hai
        recognizer.dynamic_energy_threshold = True

        try:
            audio = recognizer.listen(
                source,
                timeout=5,              # 5 sec wait karo awaaz ke liye
                phrase_time_limit=15    # max 15 sec recording
            )

            print("⏳ Processing...")
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"\nYou: {text}")
            return text.lower()         # lowercase return karo

        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unclear"
        except sr.RequestError:
            return "no_internet"
        except Exception as e:
            print(f"Listen error: {e}")
            return "error"

# ----------------------------------------
# TEST — voice.py directly run karo
# ----------------------------------------

if __name__ == "__main__":
    print("Testing TARS voice...")
    speak("Hello! I am TARS. Your AI assistant is ready.")
    print("\nNow testing microphone...")
    result = listen()
    if result not in ["timeout", "unclear", "error"]:
        speak(f"You said: {result}")