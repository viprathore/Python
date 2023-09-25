import pytest
from django.urls import reverse

from gyms.factories import GymFactory
from gyms.models import Gym


@pytest.fixture
def create_gym(db):
    gym = GymFactory()
    return gym


@pytest.mark.django_db
def test__create_gym_by_superuser(admin_auth_client):
    """
    test__create_gym_by_superuser
        test that gym is only created by the superuser only

    Args:
        admin_client (Admin): Admin user has is_superuser=True
    """

    url = reverse("gym-list")
    res = admin_auth_client.post(url, {"name": "gym 1"})

    assert res.status_code == 201
    assert Gym.objects.count() == 1


@pytest.mark.django_db
def test__gym_not_created_by_unauthorized_normal_user(client):
    """
    test__gym_not_created_by_unauthorized_normal_user
        test that gym won't be create by the normal user

    Args:
        client (User): Noraml user has is_superuser=False
    """

    url = reverse("gym-list")
    res = client.post(url, {"name": "gym 1"})

    assert res.status_code == 401
    assert Gym.objects.count() == 0


@pytest.mark.django_db
def test__gym_not_created_by_authorized_normal_user(auth_client):
    """
    test__gym_not_created_by_authorized_normal_user
        test that gym won't be create by the authorized normal user

    Args:
        client (User): Noraml user has is_superuser=False, and has valid access token
    """

    url = reverse("gym-list")
    res = auth_client.post(url, {"name": "gym 1"})

    assert res.status_code == 403
    assert Gym.objects.count() == 0


def test__get_all_gyms(auth_client, create_gym):
    """
    test__get_all_gyms
        only accessible to authorized users
    """

    res = auth_client.get(reverse("gym-list"))
    assert res.json()[0]["name"] == "Gym 1"
    assert res.status_code == 200


def test__get_all_gyms(client, create_gym):
    """
    test__get_all_gyms
        not accessible to unauthorized users
    """

    res = client.get(reverse("gym-list"))
    assert res.status_code == 401
