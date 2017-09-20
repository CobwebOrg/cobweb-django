import ipdb
from django.contrib import auth
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.forms import Form

from . import forms, models


def get_metadata_type(**kwargs):
    return models.MetadataType.objects.get_or_create(**kwargs)[0]

def get_metadata_record(**kwargs):
    # try:
    #     object_described = kwargs.pop('object_described')
    # except KeyError:
    #     kwargs.setdefault('content_type', models.Collection)

    kwargs.setdefault('object_described', get_collection())
    kwargs.setdefault('asserted_by', get_agent())
    kwargs.setdefault('metadata_type', get_metadata_type())
    kwargs.setdefault('metadata', 'this: that\tthese: those')
    test_object = models.MetadataRecord(**kwargs)
    test_object.save()
    return test_object

# def get_tag(**kwargs):
#     kwargs.setdefault('tag_property', 'test')
#     return models.Tag.objects.get_or_create(**kwargs)[0]

def get_user(**kwargs):
    kwargs.setdefault('username', 'andy')
    kwargs.setdefault('password', 'cobweb123')
    kwargs.setdefault('is_superuser', True)
    return auth.get_user_model().objects.get_or_create(**kwargs)[0]

def get_software(**kwargs):
    if kwargs:
        return models.Software.objects.get_or_create(**kwargs)[0]
    else:
        return models.Software.current_website_software()

def get_agent(**kwargs):
    kwargs.setdefault('user', get_user())
    kwargs.setdefault('software', get_software())
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





class ModelTestsMixin:

    def test_creation(self):
        self.assertTrue(isinstance(self.test_instance, self.model_class))

    def test_str(self):
        self.assertEqual(str(self.test_instance), self.test_instance.name)

class MetadataTypeModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = models.MetadataType
        self.test_instance = get_metadata_type()

class MetadataRecordModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = models.MetadataRecord
        self.test_instance = get_metadata_record()

    def test_str(self):
        string_representation = str(self.test_instance)
        self.assertIn(str(self.test_instance.object_described), string_representation)
        self.assertIn(str(self.test_instance.metadata_type), string_representation)
        self.assertIn(str(self.test_instance.asserted_by), string_representation)

# class TagModelTests(ModelTestsMixin, TestCase):
    
#     def setUp(self):
#         self.model_class = models.Tag
#         self.test_kwargs = {'tag_property': 'test', 'tag_value': 'test'}
#         self.test_instance = get_tag(**self.test_kwargs)

#     def test_str(self):
#         string_representation = str(self.test_instance)
#         self.assertIn(self.test_instance.tag_property, string_representation)
#         self.assertIn(self.test_instance.tag_value, string_representation)

#     def test_unique(self):
#         with self.assertRaises(IntegrityError):
#             doppeltag = models.Tag.objects.create(**self.test_kwargs)
#             doppeltag.save()

#     def test_adding_to_objects(self):
#         othertag = models.Tag.objects.create(tag_value='other')
#         institution = get_institution()
#         othertag.institution_set.add(institution)

#         objects_to_tag = [ 
#             institution,
#             get_user(),
#             get_software(),
#             get_project(),
#             get_nomination(),
#             get_resource(),
#             get_collection(),
#             get_claim(),
#             get_holding(),
#         ]
#         for tagobject in objects_to_tag:
#             tagobject.tags.add(self.test_instance, othertag)
#         for tagobject in objects_to_tag:
#             self.assertIn(self.test_instance, tagobject.tags.all())

#         self.assertIn(institution, othertag.institution_set.all())


class UserModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = auth.get_user_model()
        self.test_instance = get_user()

    def test_str(self):
        self.assertEqual(
            str(self.test_instance), 
            self.test_instance.get_full_name() or self.test_instance.username
        )

    def test_user_default_agent_creation(self):
        """Tests that creating a User also creates an Agent"""
        user_agent = models.Agent.objects.get(
            user=self.test_instance,
            software=models.Software.current_website_software(),
        )
        self.assertEqual(self.test_instance, user_agent.user)

class SoftwareModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = models.Software
        self.test_instance = get_software()

class AgentModelTests(ModelTestsMixin, TestCase):

    def setUp(self):
        self.model_class = models.Agent
        self.test_instance = get_agent()

    def test_str(self):
        self.assertEqual(
            str(self.test_instance),
            ', '.join([str(self.test_instance.user), str(self.test_instance.software)])
        )

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

    def setUp(self):
        self.test_instance = get_collection(archiveit_identifier="https://testurl.test/test")
        self.test_instance.full_clean()

    def test_collection_creation(self):
        self.assertTrue(isinstance(self.test_instance, models.Collection))
        self.assertEqual(str(self.test_instance), self.test_instance.name)

    def test_https_becomes_http(self):
        self.assertEqual('http://', self.test_instance.archiveit_identifier[:7])

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



class ViewTestsMixin:

    def test_load(self):
        self.assertEqual(self.test_response.status_code, 200)
        for template in self.templates:
            self.assertTemplateUsed(self.test_response, template)

class IndexViewTestsMixin(ViewTestsMixin):

    def test_list(self):
        """Index Views should list  *all* instances of a class
        (This test will have to change when we introduce pagination.)"""
        for instance in self.list_class.objects.all():
            self.assertContains(self.test_response, str(instance))
            self.assertContains(self.test_response, instance.get_absolute_url())

class DetailViewTestsMixin(ViewTestsMixin):

    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    def test_included_fields(self):
        for field in self.fields:
            # ipdb.set_trace()
            self.assertContains(self.test_response, getattr(self.test_instance, field), html=True)

    def test_update_link(self):
        pass

class HomePageTests(TestCase):

    def test_homepage(self):
        """Root URL '/' should return HTTP status 200 (i.e. success)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class UserIndexViewTests(IndexViewTestsMixin, TestCase):

    def setUp(self):
        self.list_class = models.User
        self.list_class.objects.get_or_create(username="testuser1")
        self.list_class.objects.get_or_create(username="testuser2")
        self.list_class.objects.get_or_create(username="testuser3")
        self.templates = [ 'base.html', 'user_list.html' ]
        self.test_response = self.client.get('/users/')

class UserDetailViewTests(DetailViewTestsMixin, TestCase):

    def setUp(self):
        self.test_instance = get_user()
        self.fields = [ 'username' ]
        self.templates = [ 'base.html', 'user_detail.html' ]
        self.test_response = self.client.get(self.test_instance.get_absolute_url())

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

class ProjectDetailViewTests(DetailViewTestsMixin, TestCase):

    def setUp(self):
        self.test_instance = get_project(description = "Just a test project.")
        self.fields = [ 'name', 'description' ]
        self.templates = [ 'base.html', 'project_detail.html' ]

        # Add some nominations
        self.user_nominations = {
            'facebook.com': ('user1', 'user3'),
            'linkedin.com': ('user2', 'user3'),
            'myspace.com': ('user3'),
            'twitter.com': ('user1', 'user2', 'user3'),
            'ucla.edu': ('user1', 'user3'),
        }
        for url, users in self.user_nominations.items():
            for username in users:
                get_nomination(
                    project=self.test_instance,
                    nominated_by=get_agent(user=get_user(username=username)),
                    resource=get_resource(root_url=url),
                )


        self.client.logout()
        self.test_response = self.client.get(self.test_instance.get_absolute_url())

    def test_each_nominated_resource_listed_only_once(self):
        """Each nominated resource should be listed on the Project Detail page.
        If it was nominated by multiple users, it should appear only once.

        As currently written, this test will also fail if the resource url is 
        included in a link, which shouldn't happen."""
        
        for url, users in self.user_nominations.items():
            self.assertContains(self.test_response, url, count=1)

    def test_edit_project_link(self):
        """An 'edit project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        pass

    def test_new_nomination_link(self):
        """A 'nominate' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        self.client.logout()
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(response, reverse('nominate', kwargs={'project_id': self.test_instance.pk}))

        self.client.force_login(self.test_instance.established_by.user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(response, reverse('nominate', kwargs={'project_id': self.test_instance.pk}))

    def test_username_not_agent_str(self):
        """'Created by' lists string representation of User, not Agent."""
        self.assertContains(
            self.test_response, 
            self.test_instance.established_by.user.get_full_name()
        )
        self.assertNotContains(
            self.test_response, 
            str(self.test_instance.established_by)
        )

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