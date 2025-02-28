import os
import gradio as gr
from dotenv import load_dotenv
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# Load API Keys
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

if not GROQ_API_KEY or not ELEVENLABS_API_KEY:
    raise ValueError("Missing API keys. Ensure they are set in the .env file.")

# System Prompt for AI Doctor
system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purposes. 
            What's in this image? Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, do not prescribe medicines just give a first aid idea and at the end must inform them to consult a doctor for sure,
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

# Function to process inputs
def process_inputs(audio_filepath=None, image_filepath=None):
    if audio_filepath is None and image_filepath is None:
        return "No input provided", "Please upload an image or record audio", None

    speech_to_text_output = "No audio provided"
    
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY,
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

    doctor_response = "No image provided for analysis"
    
    if image_filepath:
        encoded_img = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=f"{system_prompt} {speech_to_text_output}", 
            encoded_image=encoded_img, 
            model="llama-3.2-11b-vision-preview"
        )

    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")

    return speech_to_text_output, doctor_response, "final.mp3"

# Creating the Gradio UI
with gr.Blocks() as iface:
    gr.Markdown("# 🩺 Sympto-Sense: AI Doctor Assistant")
    
    gr.Interface(
        fn=process_inputs,
        inputs=[
            gr.Audio(sources=["microphone"], type="filepath"),
            gr.Image(type="filepath")
        ],
        outputs=[
            gr.Textbox(label="Speech to Text"),
            gr.Textbox(label="Doctor's Response"),
            gr.Audio("final.mp3")
        ]
    )
    
    with gr.Column():
       gr.HTML('<button style="background-color:rgb(195, 75, 24); color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer;" onclick="window.location.href=\'https://www.google.com/search?q=local+clinic&client=opera-gx&hs=AmY&sca_esv=3a00b5f4c73ad6fb&sxsrf=AHTn8zqot9zbV8Rgx7DoDYrCA_eSiHL7qg%3A1740704450651&ei=wgrBZ_KaJ9jvseMPwJWskA4&ved=0ahUKEwjyg8KzleWLAxXYd2wGHcAKC-IQ4dUDCBA&uact=5&oq=local+clinic&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGxvY2FsIGNsaW5pYzIEECMYJzIKEAAYgAQYQxiKBTILEAAYgAQYkQIYigUyCxAAGIAEGJECGIoFMgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIrllQoARYoARwAXgAkAEAmAF7oAHfAaoBAzAuMrgBA8gBAPgBAZgCAqAChgHCAgoQABiwAxjWBBhHmAMA4gMFEgExIECIBgGQBgiSBwMxLjGgB_MM&sclient=gws-wiz-serp\'">CONSULT DOCTOR</button>')

# Launch the Gradio App
iface.launch(debug=True)

