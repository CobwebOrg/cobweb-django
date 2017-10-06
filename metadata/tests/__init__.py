from factory import DjangoModelFactory, SubFactory, Faker

from metadata.models import Metadatum, MDProperty, MDVocabulary


class KeywordFactory(DjangoModelFactory):
    class Meta:
        model = Keyword

    name = Faker('word')

