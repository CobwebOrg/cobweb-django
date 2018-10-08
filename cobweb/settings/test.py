"""
Test-specific settings for Cobweb django site. Common settings are in base.py
"""

from cobweb.settings.production import *


DEBUG = False
TESTING = True


CRISPY_FAIL_SILENTLY = False

# ALLOWED_HOSTS += ('test',)

# DATABASES['default']['NAME'] = 'test_postgres'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr-test:8983/solr/cobweb',
        'ADMIN_URL': 'http://solr:8983/solr/admin/cores',
    },
}
