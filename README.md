# Voice Assistant 

## Overview
A simple voice assistant:
- Frontend (browser) uses Web Speech API for STT and SpeechSynthesis for TTS.
- Backend (Flask/Python) calls OpenAI Chat API to produce responses.

## Setup

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
python server.py
