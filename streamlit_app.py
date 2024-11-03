import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Add New BCA Regulatory Requirements.")
st.write( "Authorised BCA officer can upload new Requlation here– GPT will update its answer!! " )


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")

# Create an OpenAI client.
openai_api_key = st.secrets["openai"]["secret_key"]
client = OpenAI(api_key=openai_api_key)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    context = "Building and Construction Authority (BCA), Singapore Building Regulations, and BCA Submission Requirements.\n"
    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader( "Upload a document (.txt or .md)", type=("txt", "md") )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {context + document} \n\n---\n\n {question}",   #Add Prefix here....UNNI 3 Nov
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
