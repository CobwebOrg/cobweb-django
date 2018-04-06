from factory import DjangoModelFactory, Faker

from metadata import models


class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = Faker('word')
