-
title: Ai Writher
emoji: 🐠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.0.2
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
# AI Writing Assistant ✨

This project is a simple student-friendly AI Writing Assistant built with:

- Python
- Gradio
- Hugging Face Transformers
- Google Gemini API (optional)

## Tasks
- Grammar Correction
- Paraphrasing
- Summarization

## How It Works
If a GEMINI_API_KEY is provided, the app uses Google Gemini.
Otherwise, it falls back to the free `flan-t5-base` model.

## Running Locally

pip install -r requirements.txt
export GEMINI_API_KEY=your_key
python app.py
