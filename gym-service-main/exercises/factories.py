import datetime
import random
import string

import factory
import factory.fuzzy

from athletes.factories import AthleteFactory
from equipments.factories import EquipmentFactory
from exercises.models import Exercise


def get_random_calories():
    return random.randrange(10, 150)


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    name = factory.Sequence(lambda n: "Exercise {}".format(n))
    equipment = factory.SubFactory(EquipmentFactory)
    athlete = factory.SubFactory(AthleteFactory)
    duration = datetime.timedelta(minutes=get_random_calories())
    description = factory.fuzzy.FuzzyText(length=100, chars=string.ascii_letters)
    calories_burnt = factory.LazyAttribute(lambda n: get_random_calories())
