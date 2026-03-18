import streamlit as st

st.title("DocuChat 🗂️")

uploaded_file = st.file_uploader("Upload a document")


# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# chat input
if prompt := st.chat_input("Ask a question..."):
    # add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)

    # get AI response (plug your RAG pipeline here)
    response = "your RAG answer here"
    
    # add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.write(response)