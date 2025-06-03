import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from news.models import Article, Category


User = get_user_model()


@pytest.mark.django_db
def test_profile_articles_view(client):
    user = User.objects.create_user(username="testuser", password="12345")
    category = Category.objects.create(name="Tech")
    article = Article(title="My Article", content="...", category=category, author=user)
    article.save()  # вместо create()

    client.login(username="testuser", password="12345")
    url = reverse("users:profile_articles")
    response = client.get(url)

    assert response.status_code == 200
    assert b"My Article" in response.content

