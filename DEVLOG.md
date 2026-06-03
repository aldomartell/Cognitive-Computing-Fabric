
This file is a record of how this project came together — the learning process, the problems I ran into, and where I want to take it.

---

## Why J.A.R.V.I.S.

I've been an Iron Man fan for a long time. Not just the movies — the idea of a system that knows you, talks to you, and actually helps you think. J.A.R.V.I.S. in the films isn't just a voice assistant, it's an extension of Tony's mind. That stuck with me.

When I got serious about Python, I knew at some point I wanted to build something like that. Not a toy. Something that actually works, runs locally, and feels real. This project is that attempt.

---

## Where I started

I had a Python background coming in — enough to know the language, write scripts, work with libraries. But I had never touched audio programming, real-time I/O, or local LLM inference before this. Those were all new territory.

The first question I had to answer was: what does this thing actually need to do? I broke it down:

1. Hear me
2. Understand me
3. Think
4. Talk back
5. Remember what we talked about

Simple on paper. Every single one of those steps had problems I didn't expect.

---

## The audio problem

This was the hardest part of V1 by a significant margin.

Getting audio off a microphone in Python is easy. Getting it reliably, knowing when someone has stopped talking, and feeding it cleanly into a speech recognizer — that's a different problem.

My first attempts would either cut off mid-sentence or hang waiting for silence that never came. I had to figure out volume thresholds: how loud is speech versus background noise, and how long of a pause means the person is actually done talking. I ended up using a chunk-based approach, reading audio in small blocks, measuring the average amplitude of each block, and only stopping after a set number of consecutive silent chunks.

Getting those numbers right (`THRESHOLD = 350`, `SILENCE_SECS = 2.2`) took a lot of testing with my actual microphone in my actual environment. There's no universal value — you have to tune it.

The other audio issue was the TTS pipeline. `edge-tts` is async, meaning it runs on an event loop. The rest of my program is synchronous. I had to figure out how to call async code from a sync context without restructuring everything. `asyncio.run()` solved it cleanly, but understanding why that worked — and why you can't just call `await` anywhere — took time.

---

## Architecting it

Once the audio pieces were working in isolation, I had to connect everything into a loop that didn't break.

The structure I landed on:

- One function handles listening and returns text or None
- One function handles the LLM call and manages conversation history
- One function handles TTS and playback
- The main loop ties them together

Keeping those concerns separate made debugging much easier. When something broke, I knew exactly which piece to look at.

Conversation memory was another design decision. The simplest approach is to keep appending to a list forever, but that grows the context window and slows down inference over time. I implemented a rolling window — when history exceeds a limit, the oldest exchange gets dropped. It keeps the assistant fast without losing the feel of continuity.

---

## The cybersecurity angle

This project also connects to my interest in cybersecurity, which I think about more the further I get into it.

A local LLM assistant has a completely different threat model than a cloud-based one. There's no API key to leak, no data being sent to external servers, no third party logging your conversations. Everything stays on the machine. That matters.

As I build this out further, I want to explore what it means to give an AI assistant access to system tools — running commands, reading files, interacting with the network. Those capabilities open up serious attack surface. Prompt injection, privilege escalation through tool misuse, data exfiltration through a compromised model. These are real concerns and I plan to treat them seriously when I build that layer.

The intersection of AI and security is something I want to go deep on. Building J.A.R.V.I.S. is partly a way to understand that space from the inside.

---

## Where this is going

V1 works. It listens, thinks, and talks. But it's still just a conversation loop.

What I want to build toward:

- A proper interface — an Iron Man HUD in the browser, running over Flask and SocketIO, showing the assistant's responses in real time
- Persistent memory using SQLite so J.A.R.V.I.S. actually remembers things between sessions
- Wake word detection so it's always listening without me having to run a script
- Local speech recognition with Whisper so nothing touches Google's servers
- Tool use — the ability to run system commands, search the web, open applications, check files
- Eventually: a security-aware agent that can assist with reconnaissance, log analysis, and vulnerability research in a controlled lab environment

This project is long-term. V1 is the foundation.

---

*Aldo Martell — CS @ Baruch College (CUNY)*
