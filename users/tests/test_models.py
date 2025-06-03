import pytest
from django.contrib.auth import get_user_model
from users.models import Profile


User = get_user_model()


@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create_user(username="tester", password="pass1234")
    profile = user.profile  # не создаём вручную
    profile.nickname = "Тестович"
    profile.save()

    assert profile.pk is not None
    assert profile.nickname == "Тестович"
    assert profile.user == user

