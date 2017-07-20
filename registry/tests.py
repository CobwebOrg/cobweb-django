import ipdb

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


class InstitutionModelTests(TestCase):
    
    def test_institution_creation(self):
        """Tests creation of Institution objects"""
        
        t = create_institution()
        self.assertTrue(isinstance(t, Institution))
        self.assertEqual(str(t), t.name)

class AgentModelTests(TestCase):
    
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