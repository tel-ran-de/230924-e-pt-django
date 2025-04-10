import unidecode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


class ArticleQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def by_category(self, category_id):
        return self.active().filter(category_id=category_id)

    def by_tag(self, tag_id):
        return self.active().filter(tags__id=tag_id)

    def search(self, query):
        return self.active().filter(Q(title__icontains=query) | Q(content__icontains=query))

    def sorted(self, sort='publication_date', order='desc'):
        valid_sort_fields = {'publication_date', 'views'}
        if sort not in valid_sort_fields:
            sort = 'publication_date'
        order_by = f'-{sort}' if order == 'desc' else sort
        return self.active().order_by(order_by)


class AllArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def by_category(self, category_id):
        return self.get_queryset().by_category(category_id)

    def by_tag(self, tag_id):
        return self.get_queryset().by_tag(tag_id)

    def search(self, query):
        return self.get_queryset().search(query)

    def sorted(self, sort='publication_date', order='desc'):
        return self.get_queryset().sorted(sort, order)


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

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, verbose_name='Автор')

    image = models.ImageField(
        upload_to='articles/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    objects = ArticleManager()
    all_objects = AllArticleManager()

    def get_absolute_url(self):
        return reverse('news:detail_article_by_id', kwargs={'pk': self.pk})

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


class ArticleHistory(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='article_history')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} — {self.timestamp.strftime('%d %b %Y %H:%M')}"


class ArticleHistoryDetail(models.Model):
    history = models.ForeignKey(ArticleHistory, on_delete=models.CASCADE, related_name='details')
    field_name = models.CharField(max_length=100)  # например, title, category, tags и т.д.
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.field_name}: {self.old_value} → {self.new_value}"


class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Комментарий от {self.user or 'Аноним'} на {self.article.title}"

    class Meta:
        ordering = ('created_at',)


class UserSubscription(models.Model):
    """
    Подписка одного пользователя (subscriber)
    на статьи другого пользователя‑автора (author).
    """
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribed_authors",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subscriber", "author")
        verbose_name = "Подписка на автора"
        verbose_name_plural = "Подписки на авторов"

    def __str__(self):
        return f"{self.subscriber} → {self.author}"


class TagSubscription(models.Model):
    """
    Подписка пользователя на теги.
    """
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribed_tags",
    )
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subscriber", "tag")
        verbose_name = "Подписка на тег"
        verbose_name_plural = "Подписки на теги"

    def __str__(self):
        return f"{self.subscriber} → #{self.tag}"