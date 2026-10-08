# J.A.R.V.I.S.

It is an ongoing research and engineering project focused on building a persistent, cross-device AI computing agent capable of interacting through voice, text, files, applications, and external services.

The project began as a local Python voice assistant powered by an on-device LLM and is evolving into a modular agentic computing platform incorporating LLM orchestration, persistent memory, tool execution, API integrations, cross-device communication, multimodal interfaces, and autonomous workflows.

---

## Version 1.0, What it does

- Captures microphone input with automatic silence detection
- Transcribes speech using Google Speech Recognition
- Sends your input to a local Ollama LLM (`llama3.2:3b`)
- Responds with a British neural voice via Microsoft Edge TTS
- Maintains rolling conversation memory across the session
- Built-in voice commands: "exit", "shutdown", "forget everything"

---

## How it works

```
mic → silence detection → WAV
    → Google STT → text
        → Ollama (llama3.2:3b) → response
            → Edge TTS → speaker
```

---

## Stack

- Python 3.10+
- [Ollama](https://ollama.com) — local LLM inference (`llama3.2:3b`)
- `speech_recognition` — speech to text (Google STT)
- `edge-tts` — neural voice synthesis (`en-GB-RyanNeural`)
- `sounddevice` / `scipy` — audio capture and WAV handling

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
MODEL        = 'llama3.2:3b'      # swap for any Ollama model
VOICE        = "en-GB-RyanNeural" # change accent/voice
SILENCE_SECS = 2.2                # pause threshold before stopping recording
MAX_HISTORY  = 10                 # number of exchanges kept in memory
```

---

**Aldo Martell** 
