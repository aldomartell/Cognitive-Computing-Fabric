import ollama
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import tempfile
import os
import time
import asyncio
import edge_tts
import playsound

# CONFIG
MODEL         = 'llama3.2:3b'
SAMPLERATE    = 16000
THRESHOLD     = 350
SILENCE_SECS  = 2.2
MAX_SECS      = 15
MAX_HISTORY   = 10

VOICE = "en-GB-RyanNeural"

SYSTEM_PROMPT = (
    "You are J.A.R.V.I.S., Tony Stark's AI assistant. "
    "Be helpful, intelligent, slightly formal, and concise. "
    "Keep answers 1–3 sentences unless asked for detail."
)

# MEMORY 
history = []

# AI FUNCTION 
def ask_jarvis(user_text):
    history.append({"role": "user", "content": user_text})

    if len(history) > MAX_HISTORY * 2:
        del history[:2]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = ollama.chat(model=MODEL, messages=messages)
        reply = response['message']['content'].strip()

        history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"System error, sir: {e}"

# TEXT TO SPEECH (EDGE TTS - FAST + NEURAL)
async def _speak(text):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    path = tmp.name
    tmp.close()

    tts = edge_tts.Communicate(text, VOICE)
    await tts.save(path)

    playsound.playsound(path)
    os.remove(path)

def speak(text):
    print(f"\n🤖 J.A.R.V.I.S.: {text}\n")
    asyncio.run(_speak(text))

# SPEECH TO TEXT 
recognizer = sr.Recognizer()

def listen():
    chunk = 1024
    silence_lim = int(SAMPLERATE / chunk * SILENCE_SECS)
    max_chunks = int(SAMPLERATE / chunk * MAX_SECS)

    frames = []
    silent_chunks = 0
    speaking = False

    print("🎤 Listening...", end="", flush=True)

    with sd.InputStream(
        samplerate=SAMPLERATE,
        channels=1,
        dtype='int16',
        blocksize=chunk
    ) as stream:

        while len(frames) < max_chunks:
            data, _ = stream.read(chunk)
            volume = np.abs(data).mean()

            if volume > THRESHOLD:
                if not speaking:
                    print(" (heard)", end="", flush=True)

                speaking = True
                silent_chunks = 0
                frames.append(data.copy())

            elif speaking:
                frames.append(data.copy())
                silent_chunks += 1

                if silent_chunks >= silence_lim:
                    break

    print()

    if not frames:
        return None

    audio = np.concatenate(frames, axis=0)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    path = tmp.name
    tmp.close()

    wav.write(path, SAMPLERATE, audio)

    with sr.AudioFile(path) as source:
        audio_data = recognizer.record(source)

    os.remove(path)

    try:
        text = recognizer.recognize_google(audio_data)
        print(f"👤 You: {text}")
        return text
    except:
        return None

#MAIN LOOP
def main():
    speak("J.A.R.V.I.S. online. Systems ready.")

    while True:
        user_input = listen()

        if not user_input:
            continue

        lower = user_input.lower()

        if any(x in lower for x in ["exit", "shutdown", "power off", "goodbye"]):
            speak("Shutting down. Goodbye, sir.")
            break

        if "forget everything" in lower:
            history.clear()
            speak("Memory cleared, sir.")
            continue

        response = ask_jarvis(user_input)
        speak(response)

if __name__ == "__main__":
    main()