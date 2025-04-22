import streamlit as st

def main():
    st.title("Excel File Upload and SQL Query")

    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.rerun()

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        obj = load_data(uploaded_file)

        # Initialize session state variables if not already set
        if "query" not in st.session_state:
            st.session_state.query = ""
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "noun_check" not in st.session_state:
            st.session_state.noun_check = False

        # Text input
        st.session_state.query = st.text_input("Enter your query:")

        # Submit button
        if st.button("Submit"):
            st.session_state.submitted = True

        if st.session_state.submitted and st.session_state.query:
            if st.session_state.query.lower() == "exit":
                st.stop()

            # Noun check checkbox
            st.session_state.noun_check = st.checkbox("Enable noun check", value=False)

            if st.button("Submit Noun Check"):
                query = st.session_state.query
                if st.session_state.noun_check:
                    query = get_correct_query(obj, query)
                final_ans = obj.sql_agent(query)
                st.write(final_ans)

if __name__ == "__main__":
    main()