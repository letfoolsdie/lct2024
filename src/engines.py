import pandas as pd
import numpy as np
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import torch
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class DummySearch:
    def search(self, query):
        raise NotImplementedError


class ConstantDB(DummySearch):
    def search(self, query):
        return [
            {'link': 'https://cdn-st.rutubelist.ru/media/15/74/505180a547199ef368b9d1da8c5a/fhd.mp4',
            'description': None},
            {'link': 'https://cdn-st.rutubelist.ru/media/f1/42/1f759e8942c6bffab2251e2b75a1/fhd.mp4',
            'description': 'Магическая Битва 2'},
            {'link': 'https://cdn-st.rutubelist.ru/media/94/df/3c7e858a44d5a1cb2b7466575bb9/fhd.mp4',
            'description': 'Три вечерних отпускных лука 🔥 какой понравился больше всего?'},
            {'link': 'https://cdn-st.rutubelist.ru/media/6d/b1/08a9279543ac8b3962e3f8897187/fhd.mp4',
            'description': None},
            {'link': 'https://cdn-st.rutubelist.ru/media/61/2e/df3e0ab947e28e7665eed3b52038/fhd.mp4',
            'description': '#игры #видеоигры #games #videogames #blacksilverufa #нарезкистримов'},
            {'link': 'https://cdn-st.rutubelist.ru/media/05/cc/47c1c4634decaebdeca206b4fabd/fhd.mp4',
            'description': None},
            {'link': 'https://cdn-st.rutubelist.ru/media/2f/48/b934cdab4b039e27b2a2274e8736/fhd.mp4',
            'description': '#лайфхаки , #эксперименты , #roblox , #игрушки , #diy , #танцы'},
            {'link': 'https://cdn-st.rutubelist.ru/media/0a/17/2aa59ae649a6bd9169c924ca4c4c/fhd.mp4',
            'description': 'Мяч на носу 🏀🤔'},
            {'link': 'https://cdn-st.rutubelist.ru/media/85/fd/a2177e9d461a9a25af98aaefb9e3/fhd.mp4',
            'description': '#нарезкистримов , #dota2 , #cs2 , #fifa23 , #minecraft , #майнкрафт , #геншин , #genshin'},
            {'link': 'https://cdn-st.rutubelist.ru/media/cc/d9/73b3ce38422c8c8d8397c6b8f7cf/fhd.mp4',
            'description': '#boobs , #красивыедевушки , #ass'}
        ]


class ClownDB(DummySearch):
    """
    🤡 Keep everything in memory, search with sklearn cosine_similarity 🤡
    """
    def __init__(self, data_path, embeds_arr_path, model_path):
        self.data = pd.read_csv(data_path)
        self.embeds_arr = joblib.load(embeds_arr_path)
        self.model = joblib.load(model_path)
        
    def search(self, query, top_n=10):
        query_embeds = self.model.transform([query])
        sim = cosine_similarity(query_embeds, self.embeds_arr)
        top_indices = np.argsort(-sim[0])[:top_n]
        return [row.to_dict() for _, row in self.data.iloc[top_indices].iterrows()]

    
class NeuralSearcher(DummySearch):
    def __init__(
        self, 
        collection_name, 
        model_name='distiluse-base-multilingual-cased-v1',
        qdrant_url="http://localhost:6333",
        device='cuda'
    ):
        self.collection_name = collection_name
        self.model = SentenceTransformer(model_name, device=device)
        self.qdrant_client = QdrantClient(qdrant_url)
        
    def search(self, text: str):
        vector = self.model.encode(text).tolist()

        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,
            limit=10,
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function we are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads
