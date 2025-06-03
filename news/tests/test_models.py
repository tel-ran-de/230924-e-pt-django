import pytest
from news.models import Article, Category, Tag
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_article_creation():
    user = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name="Tech")
    tag = Tag.objects.create(name="Python")

    article = Article(
        title="Test Article",
        content="Content here",
        category=category,
        author=user
    )
    article.save()  # вместо create()

    article.tags.add(tag)

    assert article.pk is not None
    assert article.title == "Test Article"
    assert article.tags.count() == 1
    assert article.category.name == "Tech"
