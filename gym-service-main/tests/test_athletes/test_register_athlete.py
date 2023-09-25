import pytest
from django.urls import reverse

from athletes.models import Athlete

DUMMY_USER = {"email": "user@gmail.com", "name": "dummy user"}
DUMMY_USER_PASSWD = "testpasswd123."


@pytest.mark.django_db
def test__register_athlete(client):
    """
    test__register_athlete
        Register an athlete
    """

    res = client.post(
        reverse("athlete-list"), {"email": "athlete1@gmail.com", "password": "athlete123"}
    )

    assert res.status_code == 201
    assert Athlete.objects.count() == 1


@pytest.mark.django_db
def test__register_athlete_with_wrong_data(client):
    """
    test__register_test__register_athlete_with_wrong_data
        Register an athlete with wrong data
    """

    res = client.post(reverse("athlete-list"))

    assert res.status_code == 400
    assert Athlete.objects.count() == 0


@pytest.mark.django_db
def test__login_athlete_not_existed(client):
    """
    test__login_athlete_not_existed
        Create token for non-existed user
    """

    res = client.post(
        reverse("token_obtain_pair"),
        {"email": "unknown@gmail.com", "password": "unknownpass"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "No active account found with the given credentials"}
    assert Athlete.objects.count() == 0


@pytest.mark.django_db
def test__login_athlete_existed(client):
    user = Athlete.objects.create_user(
        **DUMMY_USER, is_superuser=False, is_staff=False, password=DUMMY_USER_PASSWD
    )

    res = client.post(
        reverse("token_obtain_pair"), {"email": user.email, "password": DUMMY_USER_PASSWD}
    )

    assert res.status_code == 200
