import pandas as pd
import numpy as np
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
from transformers import FSMTForConditionalGeneration, FSMTTokenizer
from transformers import T5ForConditionalGeneration, T5Tokenizer

import os
os.environ['HF_HOME'] = '/app/cache/'


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


class CLIPSearcher(DummySearch):
    def __init__(
        self, 
        collection_name,
        qdrant_url="http://127.0.0.1:6333",
        device='cuda'
    ):
        self.device = device
        traslator_name = "utrobinmv/t5_translate_en_ru_zh_large_1024"
        self.translate_tokenizer = T5Tokenizer.from_pretrained(traslator_name)
        self.translate_model = T5ForConditionalGeneration.from_pretrained(traslator_name).to(self.device)

        self.collection_name = collection_name
        # Initialize encoder model
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(qdrant_url)

    def translate(self, text: str):
        pass
        
    def search(self, text: str):
        input_ids = self.translate_tokenizer("translate to en: " + text, return_tensors="pt").to(self.device)
        outputs = self.translate_model.generate(**input_ids)
        text = self.translate_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0].lower()
        print()
        print(text)
        print()

        text_inp = self.processor(
            text = [text], images=None, return_tensors="pt"
        )
        text_emb = self.model.get_text_features(**text_inp).detach().numpy()[0]

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=text_emb,
            query_filter=None,  # If you don't want any filters for now
            limit=10,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads
    
    def add(self, image: np.ndarray, description: str, url: str):
        inputs = self.processor(images=[image], return_tensors="pt")
        image_feature = self.model.get_image_features(**inputs).detach().numpy()[0]

        result = self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=abs(hash(description)),
                    vector=image_feature.tolist(),
                    payload={"description": description, "link": url}
                )
            ]
        )

        return str(result.status)