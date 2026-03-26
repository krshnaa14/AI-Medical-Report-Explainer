import streamlit as st
import PyPDF2
import pytesseract
from PIL import Image
from groq import Groq

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from pdf2image import convert_from_bytes
import cv2

# ------------------ SETUP ------------------
client = Groq(api_key="ENTER_KEY_HERE")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ UI ------------------
st.set_page_config(page_title="Medical Report Explainer", layout="wide")
st.title("🩺 AI Medical Report Explainer")

# ------------------ OCR ------------------
def ocr_image(image):
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    thresh = cv2.resize(thresh, None, fx=1.5, fy=1.5)

    text = pytesseract.image_to_string(thresh, config='--psm 6')
    return text

# ------------------ TEXT EXTRACTION ------------------
def extract_text(file):
    try:
        text = ""

        if file.type == "application/pdf":
            file_bytes = file.read()

            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""

            if len(text.strip()) < 50:
                images = convert_from_bytes(file_bytes)
                text = ""
                for img in images:
                    text += ocr_image(img)

        else:
            image = Image.open(file)
            text = ocr_image(image)

        return text

    except Exception as e:
        return f"Error extracting text: {e}"

# ------------------ CHUNKING ------------------
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# ------------------ VECTOR STORE ------------------
def create_vector_store(chunks):
    if len(chunks) == 0:
        return None

    embeddings = embed_model.encode(chunks)
    embeddings = np.array(embeddings)

    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index

# ------------------ RETRIEVAL ------------------
def retrieve_context(query, chunks, index, k=3):
    query_embedding = embed_model.encode([query])
    query_embedding = np.array(query_embedding)

    D, I = index.search(query_embedding, k)
    return "\n".join([chunks[i] for i in I[0] if i < len(chunks)])

# ------------------ LLM ------------------
def generate_explanation(report, context):
    prompt = f"""
You are an experienced medical professional.

Explain the medical report clearly and simply so a normal patient can understand.

Report:
{report}

Relevant Context:
{context}

Structure:
1. Key Findings
2. What It Means
3. Severity
4. Recommended Next Steps
5. Simple Summary
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def chat(report, context, question):
    prompt = f"""
You are an experienced medical assistant.

Answer based ONLY on the report and context.

Report:
{report}

Context:
{context}

User Question:
{question}

Answer clearly and simply.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("Upload Medical Report", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("Analyzing report..."):
        report_text = extract_text(uploaded_file)

        if not report_text.strip():
            st.error("Could not read report properly. Try a clearer file.")
            st.stop()

        # RAG
        chunks = chunk_text(report_text)
        index = create_vector_store(chunks)

        if index is None:
            explanation = generate_explanation(report_text, "No context")
        else:
            context = retrieve_context("main medical findings", chunks, index)
            explanation = generate_explanation(report_text, context)

    # -------- EXPLANATION --------
    st.markdown(f"## 🧠 AI Explanation\n\n{explanation}")

    # -------- CLEAR CHAT BUTTON --------
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    # ------------------ CHAT ------------------
    st.markdown("## 💬 Chat with your Report")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask anything about your report...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        if index is not None:
            ctx = retrieve_context(user_input, chunks, index)
        else:
            ctx = "No context available"

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat(report_text, ctx, user_input)
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})