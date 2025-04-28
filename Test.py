def main():
    uploaded_file = st.file_uploader("Upload your file")

    if uploaded_file is not None:
        if "file_obj" not in st.session_state:
            st.session_state.file_obj = load_data(uploaded_file)
            st.success("File loaded!")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display previous chat messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        noun_check = st.checkbox("Enable Noun Check")
        question = st.chat_input("Ask a question about the uploaded file:")

        if question:
            with st.chat_message("user"):
                st.write(question)

            # Track if user has completed noun selection
            if noun_check:
                if "noun_selection_done" not in st.session_state or not st.session_state.noun_selection_done:
                    resp = get_correct_query(st.session_state.file_obj, question)
                    st.session_state.updated_question = resp  # Save the updated question
                    st.session_state.noun_selection_done = True
                    st.stop()  # Stop here after showing noun selection!

                # If noun selection is already done, use updated question
                question = st.session_state.updated_question

            # Now safely call get_answer
            answer = get_answer(st.session_state.file_obj, question)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)

if __name__ == "__main__":
    main()