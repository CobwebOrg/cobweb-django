from factory import DjangoModelFactory, SubFactory, Faker

from metadata.models import Metadatum, MDProperty, MDVocabulary


class MDVocabularyFactory(DjangoModelFactory):
    class Meta:
        model = MDVocabulary

    name = Faker('word')

class MDPropertyFactory(DjangoModelFactory):
    class Meta:
        model = MDProperty

    vocabulary = SubFactory(MDVocabularyFactory)
    name = Faker('word')

class MetadatumFactory(DjangoModelFactory):
    class Meta:
        model = Metadatum
        exclude = ['vocabulary']

    md_property = SubFactory(MDPropertyFactory)
    name = Faker('word')
    