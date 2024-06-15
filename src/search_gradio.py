import engines
import gradio as gr


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

def gradio_search(query: str):
    video_data = search_engine.search(query)
    html_output = ""
    for vid in video_data:
        video_html = f"""<iframe width="560" height="315" src="{vid['link']}" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>"""
        html_output += f"{vid['description']}" + "<br>" + video_html + "<br>"

    return html_output

demo = gr.Interface(
    fn=gradio_search,
    inputs=["text"],
    outputs=["html"],
)

demo.launch()
