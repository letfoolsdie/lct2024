## Docs

### Демка

Проиндексировано 110к видеороликов, полный список можно найти тут https://disk.yandex.ru/d/ahc1qzZUwxnMWA

### Запуск backend

```bash
git clone https://github.com/letfoolsdie/lct2024.git
cd lct2024
sudo docker compose up
```

### Запуск front

```bash
python -m pip install gradio
python ./src/search_gradio.py
```
на экране появится ссылка на UI (подобная этой https://c2078fcb4b89118aa6.gradio.live)

Первый запуск может занимать 5-10 минут, последующие значительно быстрее

### API Docs

https://github.com/letfoolsdie/lct2024/blob/main/api_docs.md

### Гипотезы, которые проверялись

работа с несколькими источниками данных и последующая их агрегация 

* Video2Text/Image2Text models (blip-2, Video-LLaMA, git-base, Tag2Text, etc)
* CLIP/ViClip model
* OCR (easyocr, paddleocr)
* Speech2Text (Wisper)
* text embedder (BERT multilingual base)
* translator (FSMT)


