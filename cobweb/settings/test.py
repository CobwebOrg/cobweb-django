"""
Test-specific settings for Cobweb django site. Common settings are in base.py
"""

from cobweb.settings.production import *


DEBUG = False
TESTING = True

INSTALLED_APPS += ('behave_django',)


CRISPY_FAIL_SILENTLY = False

ALLOWED_HOSTS += ('test',)

DATABASES['default']['NAME'] = 'test_postgres'

# Turn off automatic solr indexing when we add to the test db
try:
    del(HAYSTACK_SIGNAL_PROCESSOR)
except NameError:
    pass
