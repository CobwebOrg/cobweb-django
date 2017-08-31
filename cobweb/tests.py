import ipdb
from django.contrib import auth
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from . import models


def get_user(**kwargs):
    kwargs.setdefault('username', 'andy')
    kwargs.setdefault('password', 'cobweb')
    kwargs.setdefault('is_superuser', True)
    return auth.models.User.objects.get_or_create(**kwargs)[0]

def get_agent(**kwargs):
    kwargs.setdefault('name', 'Andy')
    return models.Agent.objects.get_or_create(**kwargs)[0]

# def get_agentMD(**kwargs)
#     pass

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



class ModelTests(TestCase):
    pass



class AgentModelTests(ModelTests):

    def test_agent_creation(self):
        """Tests creation of Agent objects"""

        t = get_agent()
        self.assertTrue(isinstance(t, models.Agent))
        self.assertEqual(str(t), t.name)

    def test_user_creation(self):
        """Tests that creating a User also creates an Agent"""

        t = get_user()
        self.assertTrue(isinstance(t, auth.models.User))
        user_agent = models.Agent.objects.get(user=t)
        self.assertEqual(t, user_agent.user)

class InstitutionModelTests(ModelTests):

    def test_institution_creation(self):
        """Tests creation of Institution objects"""

        t = get_institution()
        self.assertTrue(isinstance(t, models.Institution))
        self.assertEqual(str(t), t.name)

class InstitutionMDModelTests(ModelTests):
    pass

class ProjectModelTests(ModelTests):

    def test_project_creation(self):
        """Tests creation of Project objects"""

        t = get_project()
        self.assertTrue(isinstance(t, models.Project))
        self.assertEqual(str(t), t.name)

class CollectionModelTests(ModelTests):

    def test_collection_creation(self):
        t = get_collection()
        self.assertTrue(isinstance(t, models.Collection))
        self.assertEqual(str(t), t.name)

class NominationModelTests(ModelTests):

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


class ClaimModelTests(ModelTests):

    def test_claim_creation(self):
        """Tests creation of Claim objects"""

        t = get_claim()
        self.assertTrue(isinstance(t, models.Claim))
        # self.assertEqual(str(t), ",")

class HoldingModelTests(ModelTests):

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
        # self.assertTemplateUsed(self.response, 'project_list.html')
        self.assertContains(self.response, 'Boring Project')
        self.assertContains(self.response, 'Exciting Project')
        self.assertContains(self.response, 'Other Project')

    def test_new_project_link(self):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""
        pass

class ProjectDetailViewTests(TestCase):

    def setUp(self):
        self.project = get_project(name="Boring Project")
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
        pass

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

class NominationFormTests(TestCase):

    def SetUp(self):
        pass

    def test_nomination_form_links_to_resource(self):
        pass