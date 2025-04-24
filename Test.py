import streamlit as st

# Dummy function to load the uploaded file
def load_data(file):
    return "File loaded successfully"

# Dummy function to process a question
def get_answer(file_obj, question):
    return f"Answer to: '{question}' (based on {file_obj})"

def main():
    st.title("File Upload and Q&A")

    # File upload
    uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv", "txt"])

    if uploaded_file is not None:
        # Load file once
        if "file_obj" not in st.session_state:
            st.session_state.file_obj = load_data(uploaded_file)
            st.success("File loaded!")

        # Initialize chat history if not present
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display previous chat messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        question = st.chat_input("Ask a question about the uploaded file:")
        if question:
            # Store user message
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.write(question)

            # Generate and store answer
            answer = get_answer(st.session_state.file_obj, question)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)

if __name__ == "__main__":
    main()