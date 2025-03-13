import unidecode

from django.db import models
from django.utils.text import slugify


class AllArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    def sorted_by_title(self):
        return self.get_queryset().all().order_by('-title')


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Categories'  # без указания этого параметра, таблица в БД будет называться вида 'news_categorys'
        verbose_name = 'Категория'  # единственное число для отображения в админке
        verbose_name_plural = 'Категории'  # множественное число для отображения в админке
        ordering = ['name']  # указывает порядок сортировки модели по умолчанию

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Tags'  # без указания этого параметра, таблица в БД будет называться вида 'news_tags'
        verbose_name = 'Тег'  # единственное число для отображения в админке
        verbose_name_plural = 'Теги'  # множественное число для отображения в админке


class Article(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'не проверено'
        CHECKED = 1, 'проверено'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1, verbose_name='Категория')
    tags = models.ManyToManyField('Tag', related_name='article', verbose_name='Теги')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Слаг')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    status = models.BooleanField(default=0,
                                 choices=(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                 verbose_name='Проверено')

    image = models.ImageField(
        upload_to='articles/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    objects = ArticleManager()
    all_objects = AllArticleManager()

    def save(self, *args, **kwargs):
        # Сохраняем статью, чтобы получить id
        super().save(*args, **kwargs)
        if not self.slug:
            base_slug = slugify(unidecode.unidecode(self.title))
            unique_slug = base_slug
            num = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'Articles'  # без указания этого параметра, таблица в БД будет называться 'news_artcile'
        verbose_name = 'Статья'  # единственное число для отображения в админке
        verbose_name_plural = 'Статьи'  # множественное число для отображения в админке
        # ordering = ['publication_date']  # указывает порядок сортировки модели по умолчанию
        # unique_together = (...)  # устанавливает уникальность для комбинации полей
        # index_together = (...)  # создаёт для нескольких полей
        # indexes = (...)  # определяет пользовательские индексы
        # abstract = True/False  # делает модель абстрактной, не создаёт таблицу БД, нужна только для наследования другими моделями данных
        # managed = True/False  # будет ли эта модель управляться (создание, удаление, изменение) с помощью Django или нет
        # permissions = [...]  # определяет пользовательские разрешения для модели

    def __str__(self):
        return self.title


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'Like by {self.ip_address} on {self.article}'


class Favorite(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favorites')
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'Favorite by {self.ip_address} on {self.article}'