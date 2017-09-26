from factory import DjangoModelFactory, Faker

from metadata.models import Keyword


class KeywordFactory(DjangoModelFactory):
	class Meta:
		model = Keyword

	name = Faker('word')