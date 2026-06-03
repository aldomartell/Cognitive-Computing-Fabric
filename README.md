# J.A.R.V.I.S.
**Just A Rather Very Intelligent System**

A locally-running AI voice assistant inspired by Tony Stark's J.A.R.V.I.S. Fully offline LLM, neural text-to-speech, and real-time voice input — no cloud APIs, no subscriptions, runs entirely on your machine.

---

## What it does

You speak, it listens. It thinks using a local LLM and talks back with a British neural voice. No internet required after setup.

- Real-time microphone capture with automatic silence detection
- Local LLM via Ollama (`llama3.2:3b`) — nothing leaves your machine
- Neural TTS using Microsoft Edge TTS (`en-GB-RyanNeural`)
- Rolling conversation memory (last 10 exchanges)
- Voice commands: "exit", "shutdown", "forget everything"

---

## How it works

```
mic → silence detection → WAV
    → Google STT → text
        → Ollama LLM → response
            → Edge TTS → speaker
```

---

## Stack

- Python 3.10+
- [Ollama](https://ollama.com) — local LLM inference
- `speech_recognition` — speech to text
- `edge-tts` — neural voice synthesis
- `sounddevice` / `scipy` — audio capture

---

## Setup

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/jarvis.git
cd jarvis

# 2. Install dependencies
pip install ollama speechrecognition sounddevice scipy numpy edge-tts playsound

# 3. Pull the model
ollama pull llama3.2:3b

# 4. Run
python jarvis.py
```

---

## Configuration

At the top of `jarvis.py`:

```python
MODEL        = 'llama3.2:3b'      # any Ollama model works
VOICE        = "en-GB-RyanNeural" # change accent/voice
SILENCE_SECS = 2.2                # pause threshold
MAX_HISTORY  = 10                 # memory depth
```

---

## Roadmap

- Wake word detection
- Flask/SocketIO HUD interface
- SQLite persistent memory
- Whisper for local STT
- System automation tools

---

**Aldo Martell** — CS @ Baruch College (CUNY)
