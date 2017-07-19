from django.test import TestCase
from django.utils import timezone

from .models import Institution, Agent, Project, Seed, Claim, Holding


def create_institution(name="UCLA"):
    return Institution.objects.create(name=name)

def create_agent(name="Andy"):
    return Agent.objects.create(name=name)

def create_project(name="Test Project"):
    return Project.objects.create(name=name, established_by=create_agent())

def create_seed(url="twitter.com"):
    return Seed.objects.create(
        url=url,
        project = create_project(),
        nominated_by = create_agent(),
    )

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