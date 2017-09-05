import ipdb
from django.contrib import auth
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.forms import Form

from . import forms, models


def get_user(**kwargs):
    kwargs.setdefault('username', 'andy')
    kwargs.setdefault('password', 'cobweb')
    kwargs.setdefault('is_superuser', True)
    return auth.get_user_model().objects.get_or_create(**kwargs)[0]

def get_agent(**kwargs):
    kwargs.setdefault('name', 'Andy')
    return models.Agent.objects.get_or_create(**kwargs)[0]

def get_institution(**kwargs):
    kwargs.setdefault('name', 'UCLA')
    return models.Institution.objects.get_or_create(**kwargs)[0]

def get_project(**kwargs):
    kwargs.setdefault('name', 'Test Project')
    kwargs.setdefault('established_by', get_agent())
    return models.Project.objects.get_or_create(**kwargs)[0]

def get_collection(**kwargs):
    kwargs.setdefault('name', 'Test Collection')
    kwargs.setdefault('institution', get_institution())
    return models.Collection.objects.get_or_create(**kwargs)[0]

def get_resource(**kwargs):
    kwargs.setdefault('root_url', 'testproject.com')
    return models.Resource.objects.get_or_create(**kwargs)[0]

def get_nomination(**kwargs):
    kwargs.setdefault('resource', get_resource())
    kwargs.setdefault('project', get_project())
    kwargs.setdefault('nominated_by', get_agent())
    return models.Nomination.objects.get_or_create(**kwargs)[0]

def get_claim(**kwargs):
    kwargs.setdefault('resource', get_resource())
    kwargs.setdefault('collection', get_collection())
    kwargs.setdefault('asserted_by', get_agent())
    kwargs.setdefault('start_date', timezone.now())
    return models.Claim.objects.get_or_create(**kwargs)[0]

def get_holding(**kwargs):
    kwargs.setdefault('resource', get_resource())
    kwargs.setdefault('collection', get_collection())
    kwargs.setdefault('asserted_by', get_agent())
    return models.Holding.objects.get_or_create(**kwargs)[0]




class ModelTestsMixin():
    pass

class UserModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = auth.get_user_model()

class AgentModelTests(TestCase):

    def test_agent_creation(self):
        """Tests creation of Agent objects"""

        t = get_agent()
        self.assertTrue(isinstance(t, models.Agent))
        self.assertEqual(str(t), t.name)

    def test_user_creation(self):
        """Tests that creating a User also creates an Agent"""

        t = get_user()
        self.assertTrue(isinstance(t, auth.get_user_model()))
        user_agent = models.Agent.objects.get(user=t)
        self.assertEqual(t, user_agent.user)

class InstitutionModelTests(TestCase):

    def test_institution_creation(self):
        """Tests creation of Institution objects"""

        t = get_institution()
        self.assertTrue(isinstance(t, models.Institution))
        self.assertEqual(str(t), t.name)

class ProjectModelTests(TestCase):

    def test_project_creation(self):
        """Tests creation of Project objects"""

        t = get_project()
        self.assertTrue(isinstance(t, models.Project))
        self.assertEqual(str(t), t.name)

class CollectionModelTests(TestCase):

    def test_collection_creation(self):
        t = get_collection()
        self.assertTrue(isinstance(t, models.Collection))
        self.assertEqual(str(t), t.name)

class NominationModelTests(TestCase):

    def test_nomination_creation(self):
        t = get_nomination()
        self.assertTrue(isinstance(t, models.Nomination))
        # self.assertEqual(str(t), '...')

    def test_uniquetogether(self):
        """Each combination of Project, Resource, and Nominated_by is unique."""
        with self.assertRaisesRegex(IntegrityError, r'duplicate key value violates unique constraint'):
            t = get_nomination()
            models.Nomination.objects.create(
                resource = t.resource,
                project = t.project,
                nominated_by = t.nominated_by,
            )


class ClaimModelTests(TestCase):

    def test_claim_creation(self):
        """Tests creation of Claim objects"""

        t = get_claim()
        self.assertTrue(isinstance(t, models.Claim))
        # self.assertEqual(str(t), ",")

class HoldingModelTests(TestCase):

    def test_holding_creation(self):
        """Tests creation of Holding objects"""

        t = get_holding()
        self.assertTrue(isinstance(t, models.Holding))
        # self.assertEqual(str(t), "UCLA has twitter.com")



class ProjectTests(TestCase):

    def test_homepage(self):
        """Root URL '/' should return HTTP status 200 (i.e. success)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class UserIndexViewTests(TestCase):

    def setUp(self):
        pass

    def test_user_index_view(self):
        pass

class UserCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_user_create_view_fields(self):
        pass

class UserUpdateViewTests(TestCase):

    def setUp(self):
        pass

    def test_user_update_view_fields(self):
        pass

class ProjectIndexViewTests(TestCase):
    
    def setUp(self):
        get_project(name="Boring Project")
        get_project(name="Exciting Project")
        get_project(name="Other Project")
        self.response = self.client.get('/projects/')

    def test_links_to_all_projects(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'project_list.html')
        self.assertContains(self.response, 'Boring Project')
        self.assertContains(self.response, 'Exciting Project')
        self.assertContains(self.response, 'Other Project')

    def test_new_project_link(self):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""
        self.client.logout()
        self.assertNotContains(self.client.get('/projects/'), 'Create new project')
        self.assertNotContains(self.client.get('/projects/'), reverse('project_create'))
        self.client.force_login(get_user())
        self.assertContains(self.client.get('/projects/'), 'Create new project')
        self.assertContains(self.client.get('/projects/'), reverse('project_create'))

class ProjectDetailViewTests(TestCase):

    def setUp(self):
        self.user = get_user()
        self.project = get_project(name="Boring Project", established_by=self.user.agent)
        self.response = self.client.get(self.project.get_absolute_url())

    def test_detail_view(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'project_detail.html')
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Boring Project')

    def test_edit_project_link(self):
        """An 'edit project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        pass

    def test_new_nomination_link(self):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        self.client.logout()
        response = self.client.get(self.project.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(response, reverse('nominate', kwargs={'project_id': self.project.pk}))

        self.client.force_login(self.user)
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(response, reverse('nominate', kwargs={'project_id': self.project.pk}))

    # def test_seed_list(self):
    #     all_seeds = Seed.objects.all()
    #     project_seeds = self.project.seed_set.all()
    #     for seed in all_seeds:
    #         if seed in project_seeds:
    #             self.assertContains(self.response, seed.url)
    #         else:
    #             self.assertNotContains(self.response, seed.url)
    #
    # def test_no_link_to_seed_url(self):
    #     self.assertNotContains(self.response, 'href="http://nytimes.com"')

class ProjectCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_anonymous_cant_create_project(self):
        pass

    def test_user_creates_project(self):
        """...
        Should autmatically set: User"""
        pass

class NominationCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_anonymous_cannot_nominate_to_restricted_project(self):
        pass

    def test_user_creates_project(self):
        """...
        Should autmatically set: User"""
        pass



class FormTestsMixin:

    def test_init(self):
        self.form_class()

    # def test_init_without_entry(self):
    #     with self.assertRaises(KeyError):
    #         self.form_class()

    def test_with_data(self):
        for (data, valid) in self.test_data:
            form = self.form_class(data)
            self.assertEqual(form.is_valid(), valid)
      
class NominationFormTests(FormTestsMixin, TestCase):

    def setUp(self):
        self.test_object = get_nomination()
        self.form_class = forms.NominationForm

        self.test_data = [
            # ({test_data}, is_valid)
            ({'wrong_field': 'wrong info'}, False),
            ({'resource': 'twitter.com'}, True),
            ({'resource': 'http://nytimes.com', 'Description': 'NYT'}, True),
        ]

    def test_nomination_form_links_to_resource(self):
        form = forms.NominationForm({
            'resource': 'http://twitter.com',
            'project': get_project(),
            'user': get_user(),
            })
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data['resource'], models.Resource)

    def test_nomination_form_normalizes_url(self):
        form = forms.NominationForm({
            'resource': 'twitter.com',
            'project': get_project(),
            'user': get_user(),
            })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['resource'], get_resource(root_url="http://twitter.com"))