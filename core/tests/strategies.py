"""
Strategies for generation test objects using Hypothesis (http://hypothesis.works/)
"""

from hypothesis import strategies as st
from hypothesis.extra.django.models import models

from projects.models import Project, Nomination, Claim
from webresources.tests.strategies import resources


schemes = st.one_of(
    [st.just(x) for x in ('ftp', 'file', 'gopher', 'http', 'https', 'ws', 'wss')]
)

hosts = one_of(

)

@composite
def urls(draw):
    return f'{draw(schemes)}://{hosts}{paths}
