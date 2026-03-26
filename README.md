# AI-Medical-Report-Explainer
>> ⚠️ **Important:** You need a **Groq API key** to run this app. Groq offers a **free API key** — no subscription required. Make sure to sign up and add your key in `config.py` or `app.py` before running the app.

AI-powered medical report explainer with OCR, RAG-based context retrieval, and a ChatGPT-style chat interface. Upload a medical report (PDF or image), get an AI-generated explanation, and interact via chat for follow-up questions.

---

## Features

- Upload medical reports in **PDF, PNG, JPG, JPEG** formats.
- OCR-based text extraction for scanned reports.
- Retrieval-Augmented Generation (RAG) for relevant context.
- AI-generated explanations including:
  1. Key Findings
  2. What It Means
  3. Severity
  4. Recommended Next Steps
  5. Simple Summary
- Interactive chat interface to ask questions about your report.
- Clear chat button to reset the conversation.

---

## Setup / API Key

This project requires the **Groq API** for AI completions.  

1. Sign up for a Groq account: [https://console.groq.com/keys](https://console.groq.com/keys) Groq offers a free API key — no subscription required 
2. Create a **Groq API Key**.  
3. Set your API key in `config.py` (or directly in `app.py` for testing):
# config.py
GROQ_API_KEY = "your_api_key_here"

# Install Tesseract OCR and make sure the path is correct:
In app.py
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#Install dependencies:
pip install -r requirements.txt

# Usage
Run the Streamlit app:
(streamlit run app.py) 
Upload a medical report (PDF or image).
Wait for the AI explanation to appear.
Use the chat interface to ask follow-up questions.
Click the “🗑 Clear Chat” button to reset the conversation.

# Sample Reports
Use the assets/ folder for sample PDFs and images to test.
OCR may occasionally misread numbers in scanned reports. Verify critical values manually.

# Limitations
Requires a Groq API Key to function.
OCR results may vary depending on report quality.
AI explanations are for educational purposes only; not a substitute for professional medical advice.

# License
This project is licensed under the MIT License.











