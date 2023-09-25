import datetime

import pytest
from django.urls import reverse

from exercises.factories import ExerciseFactory


@pytest.fixture
def exercise(db):
    exercise = ExerciseFactory(created_at="2022-10-02")
    return exercise


def test_athlete_total_calories_valid_dates(auth_client, exercise):
    """
    test_athlete_total_calories_valid_dates
        getting total calories burnt between two valid dates
    """

    start_date = "2022-10-02"
    end_date = "2022-11-02"
    url = reverse("athlete-get-total-calories-between-dates", args=(exercise.athlete.id,))
    res = auth_client.get(f"{url}?start_date={start_date}&end_date={end_date}")

    assert res.status_code == 200


def test_athlete_total_calories_invalid_dates(auth_client, exercise):
    """
    test_athlete_total_calories_invalid_dates
        getting total calories burnt between two invalid dates
        end_date must be greater than start_date
    """

    start_date = "2023-10-02"
    end_date = "2022-11-02"
    url = reverse("athlete-get-total-calories-between-dates", args=(exercise.athlete.id,))
    res = auth_client.get(f"{url}?start_date={start_date}&end_date={end_date}")

    assert res.status_code == 400
    assert res.json() == {
        "detail": "End date must be greater than start date or Invalid date format (Must be yyyy-mm-dd)"
    }
