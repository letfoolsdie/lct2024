#from opencv_fixer import AutoFix; AutoFix()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

import engines
import urllib.request
import cv2
import os
import ffmpegcv


mname = "facebook/wmt19-ru-en"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://127.0.0.1:8001",
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
    collection_name="lct_clip_ext"
)


def get_first_frame(video_path: str, max_frames=2000):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []
    
    images = []
    frame_cnt = 0
    
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret:
            images.append(frame)
        else:
            break
        
        frame_cnt += 1
        if frame_cnt >= max_frames:
            break
    
    cap.release()
    
    frames_to_capture = [0, frame_cnt // 2, frame_cnt - 1]

    os.remove(video_path)
    
    return [cv2.cvtColor(images[index], cv2.COLOR_RGB2BGR) for index in frames_to_capture]


@app.post("/index")
async def index(url: str, desc: str):
    tmp_name = "tmp_"+str(abs(hash(url)))
    urllib.request.urlretrieve(url, tmp_name + ".mp4")
    frame = get_first_frame(tmp_name + ".mp4")
    status = clip_engine.add(frame, description=desc, url=url)
    return {"status": status}


#app.mount("/", StaticFiles(directory="/app/src/front", html=True), name="static")
