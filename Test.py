unique_key_prefix = str(uuid.uuid4())

    st.write("Select the nouns you want to use:")

    # Dynamically generate checkboxes for each noun
    selected_names = []
    for idx, name in enumerate(names):
        if st.checkbox(name, key=f"{unique_key_prefix}_{idx}"):
            selected_names.append(name)

    # Text input for manual nouns
    manual_input = st.text_input(
        "Or type your own nouns manually (comma-separated):",
        key=f"{unique_key_prefix}_manual"
    )

    # Submit button
    submit_pressed = st.button("Submit Selected or Custom Nouns", key=f"{unique_key_prefix}_submit")

    if submit_pressed:
        if manual_input.strip():
            # User entered manual nouns