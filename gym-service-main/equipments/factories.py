import factory

from equipments.models import Equipment


class EquipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Equipment

    name = factory.Sequence(lambda n: "Equipment {}".format(n))
