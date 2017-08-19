from django.test import TestCase
from django.utils import timezone

from .models import Institution, Agent, Project, Seed, Claim, Holding


def create_institution(name="UCLA"):
    return Institution.objects.create(name=name)

def create_agent(name="Andy"):
    return Agent.objects.create(name=name)

def create_project(name="Test Project", established_by=False):
    if not established_by:
        established_by = create_agent()
        established_by.save()
    return Project.objects.create(name=name, established_by=established_by)

def create_seed(url="twitter.com", nominated_by=False):
    if not nominated_by:
        nominated_by = create_agent()
        nominated_by.save()
    return Seed.objects.create(url=url, nominated_by = nominated_by,)

def create_claim():
    return Claim.objects.create(
        start_date=timezone.localdate(),
        institution=create_institution(),
        asserted_by=create_agent(),
        seed=create_seed(),
    )

def create_holding():
    return Holding.objects.create(
        institution=create_institution(),
        asserted_by=create_agent(),
        seed=create_seed(),
    )

class ModelTests(TestCase):

    def setUp(self):
        self.project = Project.objects.get(name="Boring Project")
        self.response = self.client.get(self.project.get_absolute_url())

class ProjectTests(ModelTests):

    def test_homepage(self):
        """Root URL '/' should return HTTP status 200 (i.e. success)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
class InstitutionModelTests(ModelTests):
    
    def test_institution_creation(self):
        """Tests creation of Institution objects"""
        
        t = create_institution()
        self.assertTrue(isinstance(t, Institution))
        self.assertEqual(str(t), t.name)

class AgentModelTests(ModelTests):
    
    def test_agent_creation(self):
        """Tests creation of Agent objects"""
        
        t = create_agent()
        self.assertTrue(isinstance(t, Agent))
        self.assertEqual(str(t), t.name)

class ProjectModelTests(TestCase):
    
    def test_project_creation(self):
        """Tests creation of Project objects"""
        
        t = create_project()
        self.assertTrue(isinstance(t, Project))
        self.assertEqual(str(t), t.name)

class SeedModelTests(TestCase):
    
    def test_seed_creation(self):
        """Tests creation of Seed objects"""

        t = create_seed()
        self.assertTrue(isinstance(t, Seed))
        self.assertEqual(str(t), t.url)
    
    def test_seed_in_multiple_projects(self):
        """Tests that there is a many-to-many relationship between projects and seeds."""
        
        project_1 = create_project(name="Project 1")
        project_2 = create_project(name="Project 2")
        seed_1 = create_seed(url="twitter.com")
        seed_2 = create_seed(url="nytimes.com")
        project_1.save()
        project_2.save()
        seed_1.save()
        seed_2.save()

        project_1.seed_set.add(seed_1)
        project_1.seed_set.add(seed_2)
        seed_2.project_set.add(project_2)
        
        self.assertIn(seed_1, project_1.seed_set.all())
        self.assertIn(seed_2, project_1.seed_set.all())
        self.assertNotIn(seed_1, project_2.seed_set.all())
        self.assertIn(seed_2, project_2.seed_set.all())
        
        self.assertIn(project_1, seed_1.project_set.all())
        self.assertNotIn(project_2, seed_1.project_set.all())
        self.assertIn(project_1, seed_2.project_set.all())
        self.assertIn(project_2, seed_2.project_set.all())

class ClaimModelTests(TestCase):
    
    def test_claim_creation(self):
        """Tests creation of Claim objects"""
        
        t = create_claim()
        self.assertTrue(isinstance(t, Claim))
        self.assertEqual(str(t), "UCLA claims twitter.com")

class HoldingModelTests(TestCase):
    
    def test_holding_creation(self):
        """Tests creation of Holding objects"""
        
        t = create_holding()
        self.assertTrue(isinstance(t, Holding))
        self.assertEqual(str(t), "UCLA has twitter.com")

# class ProjectIndexViewTests(TestCase):
#     fixtures = ['testdata.json']
#
#     def test_links_to_all_projects(self):
#         response = self.client.get('/projects/')
#         self.assertTemplateUsed('base.html')
#         # self.assertTemplateUsed('project_index.html')
#         self.assertContains(response, 'Boring Project')
#         self.assertContains(response, 'Exciting Project')
#         self.assertContains(response, 'Other Project')
#
# class ProjectDetailViewTests(TestCase):
#     fixtures = ['testdata.json']
#
#     def setUp(self):
#         self.project = Project.objects.get(name="Boring Project")
#         self.response = self.client.get(self.project.get_absolute_url())
#
#     def test_detail_view(self):
#         self.assertTemplateUsed(self.response, 'base.html')
#         self.assertTemplateUsed(self.response, 'project_detail.html')
#         self.assertEqual(self.response.status_code, 200)
#         self.assertContains(self.response, 'Boring Project')
#
#     def test_seed_list(self):
#         all_seeds = Seed.objects.all()
#         project_seeds = self.project.seed_set.all()
#         for seed in all_seeds:
#             if seed in project_seeds:
#                 self.assertContains(self.response, seed.url)
#             else:
#                 self.assertNotContains(self.response, seed.url)
#
#     def test_no_link_to_seed_url(self):
#         self.assertNotContains(self.response, 'href="http://nytimes.com"')