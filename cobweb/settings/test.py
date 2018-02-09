"""
Test-specific settings for Cobweb django site. Common settings are in base.py
"""

from cobweb.settings.production import *


DEBUG = False
TESTING = True
CRISPY_FAIL_SILENTLY = False

# Turn off automatic solr indexing when we add to the test db
try:
    del(HAYSTACK_SIGNAL_PROCESSOR)
except NameError:
    pass
