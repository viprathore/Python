import pytest
from django.urls import reverse

from equipments.factories import EquipmentFactory
from equipments.models import Equipment


@pytest.fixture
def create_equipment(db):
    equipment = EquipmentFactory()
    return equipment


@pytest.mark.django_db
def test__create_equipment_by_superuser(admin_auth_client):
    """
    test__create_equipment_by_superuser
        test that equipment is only created by the superuser only

    Args:
        admin_client (Admin): Admin user has is_superuser=True
    """

    url = reverse("equipment-list")
    res = admin_auth_client.post(url, {"name": "equipment 1"})

    assert res.status_code == 201
    assert Equipment.objects.count() == 1


@pytest.mark.django_db
def test__equipment_not_created_by_unauthorized_normal_user(client):
    """
    test__equipment_not_created_by_unauthorized_normal_user
        test that equipment won't be create by the normal user

    Args:
        client (User): Noraml user has is_superuser=False
    """

    url = reverse("equipment-list")
    res = client.post(url, {"name": "equipment 1"})

    assert res.status_code == 401
    assert Equipment.objects.count() == 0


@pytest.mark.django_db
def test__equipment_not_created_by_authorized_normal_user(auth_client):
    """
    test__equipment_not_created_by_authorized_normal_user
        test that equipment won't be create by the authorized normal user

    Args:
        client (User): Noraml user has is_superuser=False, and has valid access token
    """

    url = reverse("equipment-list")
    res = auth_client.post(url, {"name": "equipment 1"})

    assert res.status_code == 403
    assert Equipment.objects.count() == 0


def test__get_all_equipments(auth_client, create_equipment):
    """
    test__get_all_equipments
        only accessible to authorized users
    """

    res = auth_client.get(reverse("equipment-list"))
    assert res.json()[0]["name"] == "equipment 1"
    assert res.status_code == 200


def test__get_all_equipments(client, create_equipment):
    """
    test__get_all_equipments
        not accessible to unauthorized users
    """

    res = client.get(reverse("equipment-list"))
    assert res.status_code == 401
