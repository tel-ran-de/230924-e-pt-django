import pytest
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from users.models import Profile


User = get_user_model()


@pytest.mark.django_db
def test_user_update_form_valid():
    user = User.objects.create_user(username="testuser", email="test@example.com", password="secret")
    form = UserUpdateForm(data={
        "username": "newname",
        "first_name": "John",
        "last_name": "Doe",
        "email": "new@example.com"
    }, instance=user)
    assert form.is_valid()
    updated = form.save()
    assert updated.username == "newname"


@pytest.mark.django_db
def test_profile_update_form_valid():
    user = User.objects.create_user(username="tester", password="pass1234")
    profile = user.profile  # ✅ получаем уже существующий профиль
    form = ProfileUpdateForm(data={}, files={}, instance=profile)
    assert form.is_valid()

