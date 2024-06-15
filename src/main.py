from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import engines


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8001",
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

# search_engine = engines.ConstantDB()
# search_engine = engines.ClownDB(
#     "data/yappy_hackaton_2024_400k.csv",
#     "data/embeds_countVectorzer_1-1_word_description.joblib",
#     "data/countVectorizer_1-1_word.joblib"
# )

# search_engine = engines.NeuralSearcher(
#     collection_name="lct_clip",
#     model_name='distiluse-base-multilingual-cased-v1',
#     qdrant_url="http://localhost:6333",
#     device='cuda'
# )

search_engine = engines.CLIPSearcher(
    collection_name="lct_clip"
)

@app.get("/search")
async def search(query: str):
    return search_engine.search(query)


app.mount("/", StaticFiles(directory="front", html=True), name="static")
