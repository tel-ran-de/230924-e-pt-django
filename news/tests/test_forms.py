from news.forms import ArticleForm
from news.models import Category
import pytest


@pytest.mark.django_db
def test_article_form_valid():
    category = Category.objects.create(name="TestCat")
    form = ArticleForm(data={
        "title": "Title",
        "content": "Text",
        "category": category.id,
    })
    assert form.is_valid()
