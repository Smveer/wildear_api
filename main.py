"""
@Authors:   RENE Kevin Walson; EL HABACHI Oussama; SINGH Manveer
@Purpose:   API, main file, in run, waiting for requests
"""

from Utils.utilities import *
from Utils.library_overcoat import *
from Models.Audio import Audio
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware  # LOCAL USE ONLY


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

# LOAD WD LIBRARY
wd = ctypes.CDLL(r"Library/target/debug/libLibrary.dylib")


@app.post("/audio")
async def read_item(base64_audio: Request):
    directory = "Data"
    audio_name = "sample"
    extension = ".webm"

    audio = Audio(await base64_audio.json())  # Init the audio from json received

    audio.set_path(directory + "/" + audio_name + extension)

    create_file_from_audio(audio)  # Create the .webm file

    audio = create_wav_audio_from_webm_audio(audio)  # Convert .webm to .wav

    treat_wav_for_wildear(audio.path)

    pmc_ptr = load_pmc("Utils/pmc_data.json", [2, 1])

    prediction = predict_pmc(pmc_ptr, [0.0, 1.0], True)

    del_pmc(pmc_ptr)

    return prediction

    
    return "Segments specs created !"


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    f = open(file.filename, "wb")
    f.write(await file.read())
    f.close()
    return {"filename": file.filename}
