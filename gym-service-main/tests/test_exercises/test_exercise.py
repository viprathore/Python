import pytest
from django.urls import reverse

from athletes.factories import AthleteFactory
from equipments.factories import EquipmentFactory
from exercises.models import Exercise

EXERCISE_PAYLOAD = {
    "name": "Exercise",
    "duration": "00:30:00",
    "calories_burnt": "50",
}


@pytest.fixture
def athlete():
    return AthleteFactory()


@pytest.fixture
def equipment():
    return EquipmentFactory()


def test__create_exercises(auth_client, db, athlete, equipment):
    """
    test__create_exercises

    Args:
        auth_client (APIClient): authorized api client
        db (test_db): test db access
        athlete (Athlete): Athlete who perfoms the exercise
        equipment (Equipment): Equipment used to perform the exercise
    """

    EXERCISE_PAYLOAD["athlete"] = athlete.id
    EXERCISE_PAYLOAD["equipment"] = equipment.id
    res = auth_client.post(reverse("exercise-list"), data=EXERCISE_PAYLOAD)
    assert res.status_code == 201
    assert Exercise.objects.count() == 1


def test__get_all_exercises(auth_client, db):
    """
    test__get_all_exercises
        Get all the exercises
    """

    res = auth_client.get(reverse("exercise-list"))
    assert res.status_code == 200
