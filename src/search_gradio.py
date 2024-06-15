import requests
import gradio as gr


def gradio_search(query: str):
    video_data = requests.get("http://127.0.0.1:8000/search", params={'query': query}).json()
    html_output = ""
    for vid in video_data:
        video_html = f"""<iframe width="560" height="315" src="{vid['link']}" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>"""
        html_output += f"{vid['description']}" + "<br>" + video_html + "<br>"

    return html_output

# inp = gr.Textbox(placeholder="Ваш запрос...")
# out = gr.Textbox()

def autocomplete_fetch(query: str):
    pref_data = requests.get("http://127.0.0.1:8002/search_prefix", params={'pref': query}).json()
    if pref_data["search_result"]:
        return "\n".join(pref_data["search_result"][:5])
    return ""

# inp.change(autocomplete_fetch, inp, out)

# demo = gr.Interface(
#     fn=gradio_search,
#     inputs=[inp, out],
#     outputs=["html"],
# )


with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")

    greet_btn = gr.Button("Искать")
    out = gr.Textbox()
    greet_btn.click(fn=gradio_search, inputs=[name], outputs=gr.HTML(), api_name="greet")

    name.change(autocomplete_fetch, name, out)


demo.launch(share=True)
