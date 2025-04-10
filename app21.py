import streamlit as st
import requests
import PyPDF2
import docx

# Title
st.title("📄📚 File-Based Q&A with Groq LLM")

# Upload multiple files
uploaded_files = st.file_uploader("Upload files (PDF, TXT, DOCX)", accept_multiple_files=True)

# Input question
question = st.text_input("Ask a question based on uploaded files:")

# Groq API key
api_key = "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"
url = "https://api.groq.com/openai/v1/chat/completions"

# Extract text from files
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# When user clicks button
if st.button("Get Answer"):
    if not uploaded_files or question.strip() == "":
        st.warning("Please upload files and enter a question.")
    else:
        # Combine all file texts
        all_text = ""
        for file in uploaded_files:
            all_text += extract_text(file)

        # Create Groq API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided text."},
                {"role": "user", "content": f"Context:\n{all_text}\n\nQuestion: {question}"}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            st.success("Answer:")
            st.write(answer)
        else:
            st.error(f"Error: {response.status_code}")
            st.write(response.text)
