"""
Test-specific settings for Cobweb django site. Common settings are in base.py
"""

from cobweb.settings.base import *


DEBUG = False
TESTING = True
CRISPY_FAIL_SILENTLY = True

# Turn off automatic solr indexing when we add to the test db
del(HAYSTACK_SIGNAL_PROCESSOR)
