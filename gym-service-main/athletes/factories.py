import factory

from athletes.models import Athlete
from gyms.factories import GymFactory


class AthleteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Athlete

    name = factory.Sequence(lambda n: "Athlete {}".format(n))
    email = factory.Sequence(lambda n: "athlete{}@gmail.com".format(n))
    age = factory.Sequence(lambda n: n)
    gym = factory.SubFactory(GymFactory)
