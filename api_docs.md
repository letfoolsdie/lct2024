# API Docs

### GET /search
> метод осуществляет поиск видеороликов по текстовому описанию (не более 10 роликов)

Параметры

query: str - текст запроса


#### Пример запроса

    curl -X 'GET' \
    'http://172.20.9.14:8000/search?query=football' \
    -H 'accept: application/json'

#### Пример ответа

    [
        {
            "description": "hey",
            "link": "https://cdn-st.rutubelist.ru/media/bf/6a/f040f0dd4afc90b8eb12c8d76571/fhd.mp4"
        },
        {
            "description": "dfdf",
            "link": "https://cdn-st.rutubelist.ru/media/44/b0/eb375d264574b2b2f7392dbaaac6/fhd.mp4"
        }
    ]

### POST /index 
> метод осуществляет добавление и индексацию ролика в базу данных

Параметры

url: str - прямая ссылка до видеоролика в формате .mp4 (формат сжатия дожен поддерживаться ffmpeg)

desc: str - описание видеоролика (записывается в базу и передается при выдаче в поле description)

#### Пример запроса


    curl -X 'POST' \
    'http://172.20.9.14:8001/index?url=https%3A%2F%2Fcdn-st.rutubelist.ru%2Fmedia%2Fa3%2F9f%2F2352de2748b3868df583d51a402b%2Ffhd.mp4&desc=man%20eat%20potatoes' \
    -H 'accept: application/json' \
    -d ''

#### Пример ответа

    {
    "status": "completed"
    }


### GET /search_prefix 
> метод осуществляет поиск фраз по префиксу

Параметры

pref: str - префикс для поиска


#### Пример запроса

    curl -X 'GET' \
    'http://172.20.9.14:8002/search_prefix?pref=%D0%BC%D1%83%D0%B6' \
    -H 'accept: application/json'

#### Пример ответа

    {
        "search_result": [
            "мужчины культурно отдыхают на опушке",
            "мужчина пьет пиво и ест чебуреки",
            "мужские кальсоны"
        ]
    }
