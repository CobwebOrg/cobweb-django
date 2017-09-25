import factory

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase

from core import forms
from core.models import Agent, Software, Organization

@factory.django.mute_signals(post_save)
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        # django_get_or_create = ('username', 'password')

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    is_superuser = False

class SoftwareFactory(factory.DjangoModelFactory):
	class Meta:
		model = Software
		# django_get_or_create = ('name')

	name = factory.Faker('word')

class AgentFactory(factory.DjangoModelFactory):
	class Meta:
		model = Agent
		# django_get_or_create = ('user', 'software')

	user = factory.SubFactory(UserFactory)
	software = factory.SubFactory(SoftwareFactory)

class OrganizationFactory(factory.DjangoModelFactory):
	class Meta:
		model = Organization
		# django_get_or_create = ('name')

	name = factory.Faker('company')
	address = factory.Faker('address')
	description = factory.Faker('paragraph')
