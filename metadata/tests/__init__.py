from factory import DjangoModelFactory, SubFactory, Faker

from metadata import models


class KeywordFactory(DjangoModelFactory):
    class Meta:
        model = models.Keyword

    name = Faker('word')

