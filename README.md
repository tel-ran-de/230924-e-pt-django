# Учебный проект "Новости Info to Go"


## Урок 1

### Создали проект `itg`
1. Создали репозиторий
2. Создали проект `itg`
3. Установили зависимости `pip install django`
4. Сохранили зависимости в файл `requirements.txt` командой `pip freeze > requirements.txt`
5. 
Развернуть проект на локальной машине через командную строку:
 - Склонировать репозиторий
 - Перейти в папку проекта
 - Создать виртуальное окружение `python -m venv venv`
 - Активировать виртуальное окружение `source venv/bin/activate` на Linux/MacOS или `.\venv\Scripts\activate.bat` на Windows
 - Установить зависимости `pip install -r requirements.txt`
 - 
Либо через PyCharm:
 - Склонировать репозиторий через File -> Project from Version Control 
 - Установить зависимости через File -> Settings -> Project Interpreter или через `pip install -r requirements.txt` 

### Создание Django project
Создать проект `django-admin startproject itg .`
Этой командой мы создадим проект с именем `itg` в текущей директории.
Точка в конце команды означает, что проект будет создан в текущей директории, 
без создания дополнительной директории с именем проекта.

**commit: `Урок 1: создаём django проект`**

Запуск проекта `python manage.py runserver`
Для запуска проекта, вам нужно использовать терминал, и находясь в директории проекта, на одном уровне с файлом `manage.py`, выполнить команду `python manage.py runserver`
Для остановки сервера используйте комбинацию клавиш `Ctrl+C`

**Команды терминала:**
- `python manage.py runserver` - запуск сервера
- `cd` - смена директории
- `cd..` - переход на уровень выше
- `ls` - просмотр содержимого директории
- `pwd` - показать текущую директорию

**commit: `Урок 1: запускаем django сервер`**

Создание приложения `python manage.py startapp news`
После создания приложения, вам нужно зарегистрировать его в файле `settings.py` в разделе `INSTALLED_APPS`

**commit: `Урок 1: cоздаём django_app news`**

### Создали первое представление
```python
from django.http import HttpResponse
def main(request):
    return HttpResponse("Hello, world!")  # вернет страничку с надписью "Hello, world!"
```

Чтобы представление заработало, его нужно зарегистрировать в файле `urls.py` конфигурации проекта.

### Создали первый URL
```python
from news import views
path('', views.main),
```

Теперь, если вы перейдете на главную страницу сайта, то увидите надпись "Hello, world!"

**commit: `Урок 1: создаём первый маршрут и первое представление`**


## Урок 2

### Создаем детальное представление новости по ее ID
Для этого нам нужно создать новый маршрут, с конвертером `int`, который будет принимать `ID` новости.
```python
path('news/<int:news_id>/', views.news_detail),
```

А так же функцию, которая будет обрабатывать запрос и возвращать страницу с детальной информацией о новости.
```python
def news_by_id(request, news_id):
    return HttpResponse(f"Новость с ID {news_id}")
```

### `include` и собственный файл `urls.py` для приложения `news`
1. Создали еще одно представление `get_all_news` в файле `views.py`
2. Создали файл `urls.py` в директории приложения `news`
3. Зарегистрировали новый файл `urls.py` в файле `urls.py` конфигурации проекта с помощью функции `include`
4. Зарегистрировали маршруты без префикса `news/` в файле `urls.py` приложения `news`

**commit: `Урок 2: собственный urls.py в news и функция include`**

### Знакомство с Django Templates (Шаблоны)
1. Создали папку `templates` в директории приложения `news`
2. Создали файл `catalog.html` в директории `templates/news`
3. Переписали функцию `get_all_news` в файле `views.py` так, чтобы она возвращала страницу `catalog.html`
используя функцию `render` из модуля `django.shortcuts`

**commit: `Урок 2: рендер первого шаблона`**

### Работа с шаблоном 
1. Создали словарь с данными в `views.py` и передали его в шаблон
```python
info = {
    "users_count": 100600,
    "news_count": 1000,
}
```

2. Вставили данные в шаблон `catalog.html` с помощью шаблонного языка `Django Template Language` (`DTL`)

3. Подключили `BS5` по `CDN` и стилизовали страницу

**commit: `Урок 2: передаём первые данные в шаблон и подключил BS5`*


### Смотрим типы данных внутри шаблона

- Проверили, что можно передать только словарь
- Передали список и вывели его в шаблоне
- Передали список меню и познакомились с конструкцией `{% for item in menu %}`
- Познакомились с конструкцией `{% comment %} {% endcomment %}` для комментирования участков шаблона

**commit: `Урок 2: первый цикл в шаблоне`**

### Посмотрели на тег шаблона `if`
Сделали `<hr>` после каждого элемента списка, кроме последнего с помощью специальной переменной `forloop.last`

**commit: `Урок 2: первый тег if в шаблоне`**

### Сделали ссылки в меню кликабельными
- Передали в шаблон список словарей, где каждый словарь содержит `url` и `title`
 
**commit: `Урок 2: сделали ссылки в меню кликабельными`**

- Описали маршруты 
  `/catalog`,
  `/catalog/<int:news_id/>`,
  `/catalog/<slug:slug>`
  и создали соответствующие представления в файле `views.py`
- `catalog` возвращает `HttpResponse("Каталог новостей")`
- `get_news_by_id` возвращает `HttpResponse(f"Новость {news_id}")`
- `get_category_by_name` возвращает `HttpResponse(f"Карточка {slug}")`

**commit: `Урок 2: добавили новые маршруты`**

### Изменение структуры news/url.py` и `news/views.py`
Изменил пути и функции для дальнейшего развития проекта.
Дописали `include` в `urls.py` приложения `itg`

**commit: `Урок 2: изменение структуры путей`**

## Урок 3

### Создание базового шаблона `base.html` в корне проекта в папке `templates`
- Создали базовый шаблон `base.html` в папке `templates`
- Указали кастомный, нестандартный путь для Django в файле `settings.py` в разделе `TEMPLATES` 
- Прописали там `BASE_DIR / 'templates',`
- Подключили базовый шаблон для теста функции `main` в файле `views.py`

**commit: `Урок 3: создали базовый шаблон base.html`**

### Синтаксис блоков в шаблонах. `{% block %}` и `{% extends %}`

- Описали блок `content` в базовом шаблоне `base.html`
- Описали блок `footer` в базовом шаблоне `base.html`
- Создали шаблон `main.html` в папке `templates`, который расширяет базовый шаблон `base.html` через `{% extends %}`
- Переопределили блок `content` в шаблоне `main.html` через `{% block %}`
- Переопределили блок `footer` в шаблоне `main.html` через `{% block %}`
- Подключили шаблон `main.html` в функции `main` в файле `views.py`

**commit: `Урок 3: создали шаблон main.html и расширили базовый шаблон base.html`**

### Создание шаблона `nav_menu.html` и подключение его в базовом шаблоне через `{% include %}`

- Создали каталог `include` в папке `templates` в корне проекта
- Создали шаблон `nav_menu.html` в папке `include`
- Написали навигационное меню в шаблоне `nav_menu.html`
- Использовали шаблонный тег `{% url %}` который позволяет создавать ссылки на страницы по их именам в файле `urls.py`
- Внедрили шаблон `nav_menu.html` в базовый шаблон `base.html` через `{% include %}`
- Добавили датасет с новостями и меню, чтобы в будущем проверить работу шаблона

**commit: `Урок 3: создали шаблон nav_menu.html и внедрили его в базовый шаблон`**

### Начали работу над каталогом новостей (динамическая вставка данных в шаблон, цикл + `include`)

- Создали `include` в папке `templates` в приложении `news`
- Внутри создали шаблон `article_preview.html`
- Шаблон `article_preview.html` пока что только выводит сообщение `hello`
- Подключили шаблон `article_preview.html` в шаблоне `catalog.html` через `{% include %}`

**commit: `Урок 3: начали работу над каталогом новостей и динамической вставкой данных в шаблон`**

- Добавили шаблон `article_detail.html` в папке `templates/news` 
- Доделали `article_preview.html` в папке `templates/news`, распарсив в нём поля `title`, `category`, `tags`, `id_author`, `id_article`, `upload_date`, `views_count`, `favorites_count`
- Те же поля + `content` распарсили в `article_detail.html`
- Обновили функцию `get_detail_article_by_id` - сделали поиск статьи по `id_article` в словаре и возврат шаблона `article_detail.html` ИЛИ `404`

**commit: `Урок 3: доделали каталог новостей и детальное отображение статьи по id_article`**

### Создали папку `static` в приложении `news` и подключили статику в шаблоне `base.html`

- Создали папку `static` в приложении `news`
- Создали папку `news` в папке `static`
- В ней создали папку `css` и файл `main.css`, а так же папку `js` и файл `main.js`
- Создали тестовые стили и скрипт
- Подключили статику в шаблоне `base.html` через тег `{% load static %}` и тег `{% static %}`
- Подключили стили и скрипт в шаблоне `base.html`
- Проверили работу статики на всех страницах
- После создания и подключения статики нужно перезапустить сервер

**commit: `Урок 3: подключили статику в шаблоне base.html`**

### Собственные шаблонные теги через `simple_tag`

- Создали тег шаблона `upper_words` через `simple_tag` в файле `news/templatetags/upper_words.py`
- Протестировали его в представлении `article_detail` в шаблоне `article_detail.html`
- После создания тега и регистрации с помощью `template.Library()` нужно перезапустить сервер

**commit: `Урок 3: создал собственный тег шаблона upper_words через simple_tag`**

### Работа с фильтрами в шаблонах

Посмотрели на работу следующих фильтров в шаблоне `article_preview.html`:
- `length`
- `truncatewords`
- `join`
Так же, в шаблон был добавлен цикл для вывода тегов новости.

**commit: `Урок 3: работа с фильтрами в шаблонах`**


## Урок 4

### Инициализирующие миграции
Применили 18 стартовых миграций для создания структуры БД и настройки
`python manage.py migrate`
Инициализирующая миграция — это первая миграция, которая создается при инициализации нового приложения в Django.
Она содержит начальную структуру базы данных, основанную на моделях, определенных в вашем приложении.
Инициализирующая миграция важна для установления базовой схемы базы данных, с которой будет работать ваше приложение.
`auth`: Миграции для приложения аутентификации, которое включает модели пользователей, групп и разрешений.
`contenttypes`: Миграции для приложения, которое отслеживает типы контента в базе данных.
`sessions`: Миграции для приложения, которое управляет сессиями пользователей.
`admin`: Миграции для административного интерфейса `Django`.

**commit: `Урок 4: применение инициализирующих миграций`**

### Создаём первую модель данных
1. Описание модели
```python
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
```
2. Создание миграции
`python manage.py makemigrations`
3. Применение миграции
`python manage.py migrate`

**commit: `Урок 4: создание модели данных статьи и применение миграции`**

### Знакомство с `Shell Plus` и работа с моделью `Article` в интерактивной оболочке `Django`
- Установили `Shell Plus` командой `pip install django-extensions`
- Добавили `django_extensions` в `INSTALLED_APPS` в файле `settings.py` (перед нашим приложением `news`) 
- Запустили `Shell Plus` командой `python manage.py shell_plus`
(для отображения `SQL` запросов в консоли - `python manage.py shell_plus --print-sql`)
(для выхода из консоли `Shell Plus` - `exit()`)

**commit: `Урок 4: установка Shell Plus и подготовка ORM`**

### Загрузка данных в базу данных из JSON файла
`python manage.py loaddata articles.json`

**commit: `Урок 4: Наполнили базу данных тестовыми данными`**

#### Установили IPython, чтобы прекратить страдания:
```shell
pip install ipython
```
**commit: `Урок 4: установка ipython`**

### Операции CRUD в базе данных
```python
# Откройте Django Shell Plus
python manage.py shell_plus

# Импортируйте модель Article
from news.models import Article

# Создание новой статьи
new_article = Article(
    title="Вода стала розовой!",
    content="Вчера вода во всех реках и озерах стала розовой. Ученые обещают найти причину этого явления.",
    publication_date="2023-10-31T12:00:00Z",
    views=0
)
new_article.save()

# Чтение всех статей
all_articles = Article.objects.all()
for article in all_articles:
    print(article.title, article.content, article.publication_date, article.views)
    
# Чтение одной статьи по её ID
article = Article.objects.get(pk=1)
print(article.title, article.content, article.publication_date, article.views)

# Обновление статьи
article.title = "Обновленная абсурдная новость"
article.content = "Обновленное содержание абсурдной новости"
article.save()

# Удаление статьи
article.delete()
```
**commit: `Урок 4: Посмотрели операции CRUD через командную строку`**


## Урок 5

### Расширили модель данных тегами и категориями через связи `ForeignKey` и `ManyToManyField`
```python
class Article(models.Model):
    ...
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField('Tag', related_name='article')
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
```
### Очистили БД от старых данных с помощью команды `python manage.py flush`
### Создали миграции с помощью команды `python manage.py makemigrations`
### Применили миграции с помощью команды `python manage.py migrate`

**commit: `Урок 5: Добавили модели данных Category и Tag`**

Загрузили новые данные соответствующие новым моделям с помощью команды `python manage.py loaddata articles_2.json`

**commit: `Урок 5: Загрузка новых данных`**

### Рассмотрели примеры в `Django ORM`

```python
# Откройте Django Shell
# python manage.py shell_plus

# Создайте новый тег
new_tag = Tag(name="Новый тег")
new_tag.save()

# Создайте новую категорию
new_category = Category(name="Новая категория")
new_category.save()

# Создайте новую статью с этим тегом и категорией
new_article = Article(
    title="Новая абсурдная новость",
    content="Содержание новой абсурдной новости",
    category=new_category
)
new_article.save()
new_article.tags.add(new_tag)

# Чтение всех категорий
all_categories = Category.objects.all()
for category in all_categories:
    print(category.name)
    
# Чтение всех тегов
all_tags = Tag.objects.all()
for tag in all_tags:
    print(tag.name)
    
# Чтение всех статей
all_articles = Article.objects.all()
for article in all_articles:
    print(article.title, article.content, article.category.name, [tag.name for tag in article.tags.all()])
    
# Чтение одной категории по её ID
category = Category.objects.get(pk=1)
print(category.name)

# Чтение одного тега по его ID
tag = Tag.objects.get(pk=1)
print(tag.name)

# Чтение одной статьи по её ID
article = Article.objects.get(pk=1)
print(article.title, article.content, article.category.name, [tag.name for tag in article.tags.all()])

# Обновите тег
tag = Tag.objects.get(name="Новый тег")
tag.name = "Обновленный тег"
tag.save()

# Обновите категорию
category = Category.objects.get(name="Новая категория")
category.name = "Обновленная категория"
category.save()

# Обновите статью
article = Article.objects.get(title="Новая абсурдная новость")
article.title = "Обновленная абсурдная новость"
article.content = "Обновленное содержание абсурдной новости"
article.save()

# Обновите теги статьи
new_tag = Tag.objects.get(name="Обновленный тег")
article.tags.add(new_tag)

# Удаление категории
category = Category.objects.get(name="Обновленная категория")
category.delete()

# Удаление тега
tag = Tag.objects.get(name="Обновленный тег")
tag.delete()

# Удаление статьи
article = Article.objects.get(title="Обновленная абсурдная новость")
article.delete()
```

**commit: `Урок 5: Посмотрели операции CRUD через командную строку`**

#### Импортировали модели в `news/views.py`
```python
from .models import Article
```

#### Переписали представления для показа каталога новостей и подробного показа новости
```python
def get_all_news(request):
    articles = Article.objects.all()
    context = {
        'news': articles,
        'menu': [
            {"title": "Главная", "url": "/", "url_name": "index"},
            {"title": "О проекте", "url": "/about/", "url_name": "about"},
            {"title": "Каталог", "url": "/news/catalog/", "url_name": "catalog"},
        ],
    }
    return render(request, 'news/catalog.html', context=context)

def get_detail_article_by_id(request, article_id):
    """
    Возвращает детальную информацию по новости для представления
    """
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
        'menu': [
            {"title": "Главная", "url": "/", "url_name": "index"},
            {"title": "О проекте", "url": "/about/", "url_name": "about"},
            {"title": "Каталог", "url": "/news/catalog/", "url_name": "catalog"},
        ],
    }
    return render(request, 'news/article_detail.html', context=context)
```

**commit: `Урок 5: Подключили модели данных к представлениям`**

### Сделали ORM запросы на выборку по тегам и категориям

#### Выборка статей по категории

```python
# Пример: Получение всех статей в категории "Технологии"
category_name = "Технологии"
category = Category.objects.get(name=category_name)
articles_in_category = Article.objects.filter(category=category)
for article in articles_in_category:
    print(article.title)
```

#### Выборка статей по тегу
```python
# Пример: Получение всех статей с тегом "Инновации"
tag_name = "Инновации"
tag = Tag.objects.get(name=tag_name)
articles_with_tag = Article.objects.filter(tags=tag)
for article in articles_with_tag:
    print(article.title)
```

#### Выборка статей по категории и тегу
```python
# Пример: Получение всех статей в категории "Наука" и с тегом "Исследования"
category_name = "Наука"
tag_name = "Исследования"
category = Category.objects.get(name=category_name)
tag = Tag.objects.get(name=tag_name)
articles_in_category_and_tag = Article.objects.filter(category=category, tags=tag)
for article in articles_in_category_and_tag:
    print(article.title)
```

**commit: `Урок 5: Посмотрели операции на выборку новостей по тегу и/или категории`**