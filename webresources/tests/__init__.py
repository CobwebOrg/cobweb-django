from factory import DjangoModelFactory, Faker

from webresources.models import Resource


class ResourceFactory(DjangoModelFactory):
	class Meta:
		model = Resource
		django_get_or_create = [ 'location', ]

	location = Faker('url')