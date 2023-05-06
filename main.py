"""
@Authors:   RENE Kevin Walson; EL HABACHI Oussama; SINGH Manveer
@Purpose:   API, main file, in run, waiting for requests
"""
import base64
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware  # LOCAL USE ONLY
from Controllers import audioController
from Models.Audio import Audio

app = FastAPI()

# LOCAL USE ONLY - START
origins = [
    "http://localhost",
    "http://localhost:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# LOCAL USE ONLY - END


@app.post("/audio")
async def read_item(base64_audio: Request):
    directory = "Data"
    audio_name = "sample"
    extension = ".webm"

    # Init the audio from json received
    audio = Audio(await base64_audio.json())

    # Set path to audio, add "/" between directory path and filename
    audio.set_path(directory + "/" + audio_name + extension)

    # Create the .webm file
    audioController.create_webm(audio)

    # Convert .webm to .wav
    audio = audioController.convert_webm_to_wav(audio)

    # Create segments and delete .wav
    audioController.create_segments(audio)
    
    return "Segments created !"


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    f = open(file.filename, "wb")
    f.write(await file.read())
    f.close()
    return {"filename": file.filename}

