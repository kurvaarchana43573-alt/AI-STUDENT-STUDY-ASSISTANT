import streamlit as st
from pypdf import PdfReader
import ollama

st.set_page_config(
    page_title="AI Student Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Student Study Assistant")
st.write("Upload your study PDF and ask questions.")

# PDF Upload
uploaded_file = st.file_uploader(
    "📄 Upload your PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success("✅ PDF uploaded successfully!")

    st.write("📄 Pages:", len(reader.pages))

    question = st.text_input(
        "🔍 Ask a question from the PDF:"
    )

    if st.button("🤖 Get Answer"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            prompt = f"""
You are an AI Student Study Assistant.

Use the following study material to answer
the student's question.

STUDY MATERIAL:
{text[:15000]}

QUESTION:
{question}

Give a simple and clear answer.
"""

            try:

                with st.spinner("🤔 Thinking..."):

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                st.subheader("🤖 Answer")
                st.write(response["message"]["content"])

            except Exception as e:

                st.error("❌ Ollama error")
                st.write(e)

else:

    st.info("👆 Please upload a PDF to start.")