import requests
import gradio as gr


def gradio_search(query: str):
    video_data = requests.get("http://127.0.0.1:8000/search", params={'query': query}).json()
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

demo.launch(share=True)
