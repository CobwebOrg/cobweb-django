"""
Strategies for generation test objects using Hypothesis (http://hypothesis.works/)
"""

from hypothesis import strategies as st
from hypothesis.extra.django.models import models

from projects.tests.factories import ClaimFactory
from projects.models import Project, Nomination, Claim
from webresources.tests.factories import ResourceFactory


def generate_with_claims(nomination):
    """
    Magic formula for generating with dependent models.
    cf. http://hypothesis.readthedocs.io/en/latest/django.html#generating-child-models
    """
    return st.lists(
        builds(ClaimFactory, nomination=st.just(nomination), collection=st.builds(CollectionFactory)),
        min_size=0, average_size=2,
    ).map(lambda _: nomination)


nominations = models(
    Nomination,
    project=models(Project),
    resource=st.builds(ResourceFactory),
).flatmap(generate_with_claims)
