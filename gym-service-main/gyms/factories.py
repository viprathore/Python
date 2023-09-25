import factory

from gyms.models import Gym


class GymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gym

    name = factory.Sequence(lambda n: "Gym {}".format(n))
