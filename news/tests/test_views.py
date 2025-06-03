import pytest
from django.urls import reverse
from news.models import Article, Category


@pytest.mark.django_db
def test_catalog_view(client):
    category = Category.objects.create(name="Science")
    article = Article(
        title="Article A",
        content="...",
        category=category
    )
    article.save()

    url = reverse("news:catalog")
    response = client.get(url)

    assert response.status_code == 200
    assert b"Article A" in response.content
