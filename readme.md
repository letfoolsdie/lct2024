## Docs

![diagrams_image](https://github.com/letfoolsdie/lct2024/assets/15076754/a91eee43-eb91-4c01-8f4e-3ce2d809e15e)

Общий документ https://disk.yandex.ru/i/tpB3kKTms3E3zA

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

### Скорость работы

Сервер: NVIDIA GeForce RTX 4090; Intel i7-13700KF; Ubuntu 22.04.4 LTS

search метод: translator (86 ms) + clip (6 ms) + index (3 ms) = 95 ms

index метод: 250 ms

### API Docs

https://github.com/letfoolsdie/lct2024/blob/main/api_docs.md

pdf-формат https://disk.yandex.ru/i/tWVCIUXtZpd1YA

### Гипотезы, которые проверялись

работа с несколькими источниками данных и последующая их агрегация 

* Video2Text/Image2Text models (blip-2, Video-LLaMA, git-base, Tag2Text, etc)
* CLIP/ViClip model
* OCR (easyocr, paddleocr)
* Speech2Text (Wisper)
* text embedder (BERT multilingual base)
* translator (FSMT, T5)


