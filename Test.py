import streamlit as st

def main():
    st.title("Excel File Upload and SQL Query")

    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.rerun()

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        obj = load_data(uploaded_file)

        # Initialize session state
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "noun_submitted" not in st.session_state:
            st.session_state.noun_submitted = False

        if not st.session_state.submitted:
            query = st.text_input("Enter your query:")
            if st.button("Submit"):
                if query:
                    st.session_state.query = query
                    st.session_state.submitted = True
        else:
            query = st.session_state.query
            if query.lower() == "exit":
                st.write("Session ended.")
                st.stop()

            noun_check = st.checkbox("Enable noun check", value=False, key="noun_check")

            if st.button("Submit Noun Check"):
                if noun_check:
                    query = get_correct_query(obj, query)
                final_ans = obj.sql_agent(query)
                st.write(final_ans)
                st.session_state.noun_submitted = True

            if st.session_state.noun_submitted:
                if st.button("New Query"):
                    # Reset state for new input
                    st.session_state.submitted = False
                    st.session_state.noun_submitted = False
                    st.session_state.query = ""

if __name__ == "__main__":
    main()