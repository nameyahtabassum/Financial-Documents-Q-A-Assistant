import streamlit as st
import pandas as pd
import fitz  
import ollama

# -------- PDF Extraction --------
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# -------- Excel Extraction --------
def extract_text_from_excel(file):
    df = pd.read_excel(file)
    return df.to_string()

# -------- Ask LLM --------
def ask_llm(prompt):
    response = ollama.chat(model="stablelm2:1.6b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# -------- Streamlit App --------s
st.set_page_config(page_title="Financial Document Q&A", layout="wide")
st.title("📊 Financial Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload a PDF or Excel file", type=["pdf", "xlsx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(uploaded_file)
    else:
        extracted_text = extract_text_from_excel(uploaded_file)

    st.subheader("Extracted Content Preview")
    st.text_area("File Content", extracted_text[:2000], height=200)

    query = st.text_input("Ask a question about this document:")
    if st.button("Get Answer") and query:
        final_prompt = f"""
        Answer the following question based on this document:

        Document Content:
        {extracted_text}

        Question: {query}
        """
        answer = ask_llm(final_prompt)
        st.subheader("Answer")
        st.write(answer)
