# Интерактивная карта Москвы

Веб-приложение для отображения интересных мест Москвы на интерактивной карте с подробными описаниями и галереей фотографий.

![Python Version](https://img.shields.io/badge/python-3.10-blue)
![Django Version](https://img.shields.io/badge/django-4.2.7-green)

**[Демо сайта](https://isking.pythonanywhere.com)**

## Технический стек

- **Backend:** Django 4.2.7, Django REST Framework
- **Frontend:** Leaflet.js, JavaScript
- **База данных:** SQLite
- **Дополнительно:** django-admin-sortable2, django-ckeditor, python-decouple, Pillow

## Ключевые особенности реализации

### 1. Оптимизация запросов к БД
Использование `prefetch_related` для предотвращения N+1 запросов при получении связанных изображений:

```python
Place.objects.prefetch_related('images').all()
```

### 2. RESTful API
Реализованы два endpoint для работы с данными:

- `GET /places/` - GeoJSON с координатами всех мест
- `GET /places/<id>/` - детальная информация о конкретном месте

```python
def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    imgs = [request.build_absolute_uri(img.image.url) for img in place.images.all()]
    return JsonResponse({
        "title": place.title,
        "imgs": imgs,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {"lng": str(place.lng), "lat": str(place.lat)}
    })
```

### 3. Удобная админ-панель
- Inline-редактирование связанных изображений
- Drag-and-drop сортировка фотографий через django-admin-sortable2
- WYSIWYG-редактор для rich-text описаний

```python
class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
```

### 4. Управление конфигурацией
Вынос чувствительных данных в переменные окружения через python-decouple:

```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

### 5. Модели данных
Связь один-ко-многим между местами и изображениями с сортировкой:

```python
class Place(models.Model):
    title = models.CharField(max_length=200)
    lng = models.FloatField()
    lat = models.FloatField()
    description_short = models.TextField(blank=True)
    description_long = RichTextField(blank=True)

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='places/')
    position = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['position']
```

## Структура проекта

```
afisha-pelid-team/
├── places/
│   ├── models.py        # Модели Place и Image
│   ├── views.py         # API views с оптимизацией запросов
│   └── admin.py         # Настройка админки с inline и сортировкой
├── where_to_go/
│   ├── settings.py      # Конфигурация с переменными окружения
│   └── urls.py
├── templates/
├── static/
├── media/
└── requirements.txt
```

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/ваш_username/afisha-pelid-team.git
cd afisha-pelid-team
```

2. Создать виртуальное окружение и установить зависимости:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Настроить переменные окружения в `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

4. Применить миграции и создать суперпользователя:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Запустить сервер:
```bash
python manage.py runserver
```

## API Endpoints

### GET /places/
Возвращает GeoJSON со всеми местами:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [37.64, 55.75]
      },
      "properties": {
        "title": "Название места",
        "placeId": 1,
        "detailsUrl": "/places/1/"
      }
    }
  ]
}
```

### GET /places/\<id\>/
Возвращает детальную информацию о месте с изображениями:
```json
{
  "title": "Название места",
  "imgs": [
    "https://example.com/media/places/image1.jpg",
    "https://example.com/media/places/image2.jpg"
  ],
  "description_short": "Краткое описание",
  "description_long": "<p>Полное описание с HTML</p>",
  "coordinates": {
    "lng": "37.64",
    "lat": "55.75"
  }
}
```

## Деплой

Проект развернут на PythonAnywhere с использованием:
- WSGI-конфигурации для Django
- Виртуального окружения Python 3.10
- Переменных окружения для production-настроек

## Что реализовано

✅ REST API с GeoJSON  
✅ Оптимизация запросов (prefetch_related)  
✅ Админка с inline и drag-and-drop  
✅ WYSIWYG-редактор для контента  
✅ Управление конфигурацией через .env  
✅ Деплой на production

## Цель проекта

Учебный проект для демонстрации навыков работы с Django и REST API.