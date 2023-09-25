"""
/conftest.py
~~~~~~~~~~~~

Defines project-scope Pytest fixtures.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from athletes.models import Athlete

DUMMY_USER = {"email": "user@gmail.com", "name": "dummy user"}
DUMMY_USER_PASSWD = "testpasswd123."

SUPER_USER = {
    "email": "super_user@gmail.com",
    "name": "super user",
    "is_active": True,
    "is_superuser": True,
    "is_staff": True,
    "password": DUMMY_USER_PASSWD,
}


@pytest.fixture
def dummy_user(db):
    user = Athlete.objects.create_user(**DUMMY_USER, password=DUMMY_USER_PASSWD)
    return user


@pytest.fixture
def auth_client(db):
    user = Athlete.objects.create_user(
        **DUMMY_USER, is_superuser=False, is_staff=False, password=DUMMY_USER_PASSWD
    )

    client = APIClient()
    res = client.post(
        reverse("token_obtain_pair"), {"email": user.email, "password": DUMMY_USER_PASSWD}
    )
    assert res.status_code == 200

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def admin_auth_client(db):
    superuser = Athlete.objects.create_user(**SUPER_USER)
    client = APIClient()

    res = client.post(
        reverse("token_obtain_pair"),
        {"email": superuser.email, "password": DUMMY_USER_PASSWD},
    )
    assert res.status_code == 200
    # Obtain token for user
    refresh = RefreshToken.for_user(superuser)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
