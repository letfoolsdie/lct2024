from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import engines

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# search_engine = engines.ConstantDB()
search_engine = engines.ClownDB(
    "data/yappy_hackaton_2024_400k.csv",
    "data/embeds_countVectorzer_1-1_word_description.joblib",
    "data/countVectorizer_1-1_word.joblib"
)

@app.get("/search")
async def search(query: str):
    return search_engine.search(query)
