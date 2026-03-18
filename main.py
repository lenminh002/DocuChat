import streamlit as st
from rag import rag_pipeline

st.title("DocuChat 🗂️")

# initialize
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    if uploaded_file.name != st.session_state.get("uploaded_file_name"):
        st.session_state.messages = []  # reset chat for new document
        st.session_state.uploaded_file_name = uploaded_file.name

uploaded_file = st.session_state.uploaded_file


# initialize and displaychat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])



# disable chat input if no document uploaded
if uploaded_file is None:
    st.info("Please upload a document to start chatting.")
    prompt = st.chat_input("Ask a question about the document", disabled=True)
else:
    prompt = st.chat_input("Ask a question about the document")


# chat input
if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        response = rag_pipeline(uploaded_file, prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)