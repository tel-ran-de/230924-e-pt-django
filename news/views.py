import json

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView


from .forms import ArticleForm, ArticleUploadForm
from .models import Article, Favorite, Category, Like, Tag

import unidecode
from django.db import models
from django.utils.text import slugify


"""
Информация в шаблоны будет браться из базы данных
Но пока, мы сделаем переменные, куда будем записывать информацию, которая пойдет в 
контекст шаблона
"""
# Пример данных для новостей

info = {
    "users_count": 5,
    "news_count": 10,
    "categories": Category.objects.all(),
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/news/catalog/",
         "url_name": "news:catalog"},
        {"title": "Добавить статью",
         "url": "/news/add/",
         "url_name": "news:add_article"},
        {"title": "Избранное",
         "url": "/news/favorites/",
         "url_name": "news:favorites"},
    ],
}


class UploadJsonView(FormView):
    template_name = 'news/upload_json.html'
    form_class = ArticleUploadForm
    success_url = '/news/catalog/'

    def form_valid(self, form):
        json_file = form.cleaned_data['json_file']
        try:
            data = json.load(json_file)
            errors = form.validate_json_data(data)
            if errors:
                return self.form_invalid(form)
            self.request.session['articles_data'] = data
            self.request.session['current_index'] = 0
            return redirect('news:edit_article_from_json', index=0)
        except json.JSONDecodeError:
            form.add_error(None, 'Неверный формат JSON-файла')
            return self.form_invalid(form)


class EditArticleFromJsonView(FormView):
    template_name = 'news/edit_article_from_json.html'
    form_class = ArticleForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        index = self.kwargs['index']
        articles_data = self.request.session.get('articles_data', [])
        if index >= len(articles_data):
            return redirect('news:catalog')
        article_data = articles_data[index]
        kwargs['initial'] = {
            'title': article_data['fields']['title'],
            'content': article_data['fields']['content'],
            'category': Category.objects.get(name=article_data['fields']['category']),
            'tags': [Tag.objects.get(name=tag) for tag in article_data['fields']['tags']]
        }
        return kwargs

    def form_valid(self, form):
        index = self.kwargs['index']
        articles_data = self.request.session.get('articles_data', [])
        article_data = articles_data[index]

        if 'next' in self.request.POST:
            save_article(article_data, form)
            self.request.session['current_index'] = index + 1
            return redirect('news:edit_article_from_json', index=index + 1)
        elif 'save_all' in self.request.POST:
            save_article(article_data, form)
            for i in range(index + 1, len(articles_data)):
                save_article(articles_data[i])
            del self.request.session['articles_data']
            del self.request.session['current_index']
            return redirect('news:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        index = self.kwargs['index']
        articles_data = self.request.session.get('articles_data', [])
        context['index'] = index
        context['total'] = len(articles_data)
        context['is_last'] = index == len(articles_data) - 1
        return context


def save_article(article_data, form=None):
    fields = article_data['fields']
    title = fields['title']
    content = fields['content']
    category_name = fields['category']
    tags_names = fields['tags']
    category = Category.objects.get(name=category_name)
    # Генерируем slug до создания статьи
    base_slug = slugify(unidecode.unidecode(title))
    unique_slug = base_slug
    num = 1
    while Article.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    if form:
        article = form.save(commit=False)
        article.slug = unique_slug
        article.save()
        # Обновляем теги
        article.tags.set(form.cleaned_data['tags'])
    else:
        article = Article(
            title=title,
            content=content,
            category=category,
            slug=unique_slug
        )
        article.save()
        # Добавляем теги к статье
        for tag_name in tags_names:
            tag = Tag.objects.get(name=tag_name)
            article.tags.add(tag)
    return article


class FavoritesView(ListView):
    model = Article
    template_name = 'news/catalog.html'
    context_object_name = 'news'
    paginate_by = 20

    def get_queryset(self):
        ip_address = self.request.META.get('REMOTE_ADDR')
        return Article.objects.filter(favorites__ip_address=ip_address)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        article = self.get_object()

        viewed_articles = request.session.get('viewed_articles', [])
        if article.id not in viewed_articles:
            article.views += 1
            article.save()
            viewed_articles.append(article.id)
            request.session['viewed_articles'] = viewed_articles

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class ToggleFavoriteView(View):
    def post(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        ip_address = request.META.get('REMOTE_ADDR')
        favorite, created = Favorite.objects.get_or_create(article=article, ip_address=ip_address)
        if not created:
            favorite.delete()
        return redirect('news:detail_article_by_id', pk=article_id)


class ToggleLikeView(View):
    def post(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        ip_address = request.META.get('REMOTE_ADDR')
        like, created = Like.objects.get_or_create(article=article, ip_address=ip_address)
        if not created:
            like.delete()
        return redirect('news:detail_article_by_id', pk=article_id)


class SearchNewsView(ListView):
    model = Article
    template_name = 'news/catalog.html'
    context_object_name = 'news'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class GetNewsByTagView(ListView):
    model = Article
    template_name = 'news/catalog.html'
    context_object_name = 'news'
    paginate_by = 20

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        tag = get_object_or_404(Tag, pk=tag_id)
        return Article.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class GetNewsByCategoryView(ListView):
    model = Article
    template_name = 'news/catalog.html'
    context_object_name = 'news'
    paginate_by = 20

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        return Article.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


class GetAllNewsViews(ListView):
    model = Article
    template_name = 'news/catalog.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # считаем параметры из GET-запроса
        sort = self.request.GET.get('sort', 'publication_date')  # по умолчанию сортируем по дате загрузки
        order = self.request.GET.get('order', 'desc')  # по умолчанию сортируем по убыванию

        # Проверяем дали ли мы разрешение на сортировку по этому полю
        valid_sort_fields = {'publication_date', 'views'}
        if sort not in valid_sort_fields:
            sort = 'publication_date'

        # Обрабатываем направление сортировки
        order_by = f'-{sort}' if order == 'desc' else sort

        return Article.objects.select_related('category').prefetch_related('tags').order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['user_ip'] = self.request.META.get('REMOTE_ADDR')
        return context


def get_detail_article_by_title(request, title):
    """
    Возвращает детальную информацию по новости для представления
    """
    article = get_object_or_404(Article, slug=title)

    context = {**info, 'article': article, 'user_ip': request.META.get('REMOTE_ADDR'),}

    return render(request, 'news/article_detail.html', context=context)

class AddArtilceView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/add_article.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.slug = self.generate_unique_slug(form.cleaned_data['title'])
        article.save()
        form.save_m2m()

        return redirect('news:detail_article_by_id', pk=article.id)

    def generate_unique_slug(self, title):
        base_slug = slugify(unidecode.unidecode(title))
        unique_slug = base_slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        return unique_slug


def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news:detail_article_by_id', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form, 'menu': info['menu'], 'article': article}
    return render(request, 'news/edit_article.html', context=context)


def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == "POST":
        article.delete()
        return redirect('news:catalog')

    context = {'menu': info['menu'], 'article': article}
    return render(request, 'news/delete_article.html', context=context)
