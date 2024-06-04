### Инструкция )))

 - Готовим эмбеды из описания видео для qdrant. Пример в ноутбуке qdrant_lct_baseline.ipynb.
 - Запускаем qdrant: `docker run -p 6333:6333 -p 6334:6334     -v $(pwd)/qdrant_storage:/qdrant/storage:z  qdrant/qdrant`
 - Далее запускаем fastapi сервер:
    ```
    cd src
    fastapi dev main.py

    http://127.0.0.1:8000/search?query=test
    ```
    Для прода (чтобы сервис был доступен не только локально) заменить `fastapi dev main.py` на `fastapi run`.
   
    UI должен быть доступен по http://127.0.0.1:8000/
