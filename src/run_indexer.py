from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

import engines
import urllib.request
import cv2


mname = "facebook/wmt19-ru-en"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8002",
    "http://127.0.0.1:8002",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clip_engine = engines.CLIPSearcher(
    collection_name="lct_clip"
)

def get_first_frame(name: str):
    cap = cv2.VideoCapture(name)
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame


@app.get("/add")
async def add(url: str, disc: str):
    tmp_name = str(abs(hash(url)))
    urllib.request.urlretrieve(url, tmp_name + ".mp4")
    frame = get_first_frame(tmp_name + ".mp4")
    status = clip_engine.add(frame, discription=disc, url=url)
    return {"status": status}


app.mount("/", StaticFiles(directory="front", html=True), name="static")
