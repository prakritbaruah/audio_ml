import os

import google.generativeai as genai
import streamlit as st


# Set the title of the app
st.title("Audio ML")

# Add a file uploader to allow users to upload audio files
uploaded_files = st.file_uploader(
    "Upload Audio Files",
    type=['wav', 'mp3', 'ogg', 'flac', 'aac'],
    accept_multiple_files=True
)

# Check if any files have been uploaded
if uploaded_files:
    # Create a list to hold the file names
    file_names = [uploaded_file.name for uploaded_file in uploaded_files]

    # Let the user select an uploaded file to play
    selected_audio = st.selectbox("Select an audio file to play", file_names)

    # Find the corresponding UploadedFile object
    selected_file = next(
        (file for file in uploaded_files if file.name == selected_audio),
        None
    )

    if selected_file:
        # Read the audio data
        audio_bytes = selected_file.read()

        # Determine the file extension and set the appropriate audio format
        file_extension = os.path.splitext(selected_file.name)[1][1:].lower()
        audio_format = f"audio/{file_extension}"

        # Display audio player
        st.audio(audio_bytes, format=audio_format)

        # Save audio to tmp location
        save_path = os.path.join("tmp", selected_file.name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(audio_bytes)
        st.success(f"File saved to {save_path}")

        st.subheader("Audio Analysis")

        # Select prompt for LLM
        llm_prompts = {
            "Describe": "Describe this audio clip",
            "Transcribe": "Generate a transcript of the audio clip",
            "Determine mood": "Pick a single word to describe the mood of the speaker in the audio clip"
        }

        selected_prompt_key = st.selectbox("Select an action for the audio clip", llm_prompts.keys())

        if selected_prompt_key:
            selected_prompt = llm_prompts[selected_prompt_key]
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

            myfile = genai.upload_file(save_path)

            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content([myfile, selected_prompt])
            
            st.write("AI results:\n", result.text)
else:
    st.info("Please upload one or more audio files.")