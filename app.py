import gradio as gr
from transformers import pipeline
import google.generativeai as genai

# ----------------------------------------------------------
# 1. Setup GEMINI (API key stored as HF secret environment variable)
# ----------------------------------------------------------
import os
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")
else:
    gemini_model = None

# ----------------------------------------------------------
# 2. Fallback Model (free HF model so app always works)
# ----------------------------------------------------------
fallback_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

# ----------------------------------------------------------
# 3. Function Logic
# ----------------------------------------------------------
def writing_assistant(task, text):
    if not text.strip():
        return "Please enter some text."

    # Task prompts
    prompts = {
        "Grammar Correction": f"Correct the grammar:\n{text}",
        "Paraphrasing": f"Paraphrase clearly:\n{text}",
        "Summarization": f"Summarize this:\n{text}"
    }

    prompt = prompts.get(task, "")

    # Try Gemini first (if key exists)
    if gemini_model:
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception:
            pass  # if gemini fails, fallback is used

    # Fallback to Free HF Model
    output = fallback_model(prompt, max_length=200)[0]["generated_text"]
    return output


# ----------------------------------------------------------
# 4. Simple UI with Download Button
# ----------------------------------------------------------
def download_output(text):
    return text

with gr.Blocks() as demo:
    gr.Markdown("# ✨ AI Writing Assistant\n### Grammar Correction • Paraphrasing • Summarization\nA simple student-friendly writing helper.")

    task = gr.Dropdown(
        ["Grammar Correction", "Paraphrasing", "Summarization"],
        label="Select Task",
        value="Grammar Correction"
    )

    input_text = gr.Textbox(
        lines=6,
        label="Enter your text here"
    )

    output_text = gr.Textbox(
        lines=6,
        label="AI Result"
    )

    generate_btn = gr.Button("Generate")
    download_btn = gr.DownloadButton(
        label="Download "
    )

    # Generate button action
    def process_and_prepare(task, text):
        result = writing_assistant(task, text)
        return result, result  # result to textbox and to download file

    generate_btn.click(
        fn=process_and_prepare,
        inputs=[task, input_text],
        outputs=[output_text, download_btn]
    )

demo.launch(share=True)
