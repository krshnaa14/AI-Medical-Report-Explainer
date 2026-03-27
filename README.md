## 🧠 AI Medical Report Explainer

This project is a simple AI tool that helps users understand medical reports.
You can upload a PDF or image, and it will extract the text, analyze it, and explain it in an easy-to-understand way.

It also has a chat feature so you can ask follow-up questions about your report.

## 🚀 What it does 

Upload medical reports (PDF, PNG, JPG, JPEG)
Extracts text using OCR (Tesseract)
Uses RAG to get better context before generating answers
Gives structured output like:
Key Findings
What it means
Severity
Next steps
Simple summary
Chat interface to ask more questions
Option to clear chat and start fresh

## 🧠 How it works (high-level)

Basically the flow is:

Upload → OCR → clean text → split into chunks → convert to embeddings → store → retrieve relevant parts → send to LLM → generate answer

I used RAG here so the model doesn’t just guess and instead uses actual content from the report.

# 📦 RAG details
Chunk size is around 300–500 tokens
Retrieves top 3–5 relevant chunks
Uses embeddings + vector search (FAISS/Chroma)
Then passes that context to the LLM (Groq)

# ⚙️ Why I built it this way
Used Groq API because it’s fast for chat-based apps
Added OCR since many reports are scanned images
Used structured output so it’s easier to read instead of a big paragraph
Added chat so users can interact instead of just getting one response

# 🛠️ Tech stack
Python
Streamlit
Groq API
Tesseract OCR
FAISS / Chroma

# 🔑 Setup

You’ll need a Groq API key (it’s free).

Go to: https://console.groq.com/keys
Create a key
Add it in config.py:
GROQ_API_KEY = "your_api_key_here"

Install dependencies:

pip install -r requirements.txt

Install Tesseract and set path in app.py:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

▶️ Run the app
streamlit run app.py

Then:
Upload a report
Wait for explanation
Ask questions in chat

# ⚠️ Limitations
OCR is not perfect (especially for low-quality scans)
Sometimes numbers might be slightly off
LLM can still make mistakes
Not meant for real medical decisions

# 🔮 Things I’d improve later
Add citations for answers
Improve OCR accuracy
Add confidence scores
Maybe deploy it as a proper web app

# 📄 License

MIT License

# 🎥 Demo

(I’ll add a demo video or screenshots here soon)






