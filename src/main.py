from fastapi import FastAPI
import engines

app = FastAPI()
# search_engine = engines.ConstantDB()
search_engine = engines.ClownDB(
    "data/yappy_hackaton_2024_400k.csv",
    "data/embeds_countVectorzer_1-1_word_description.joblib",
    "data/countVectorizer_1-1_word.joblib"
)

@app.get("/search")
async def search(query: str):
    return search_engine.search(query)
