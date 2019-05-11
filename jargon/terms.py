import yaml
from django.conf import settings

with open(settings.BASE_DIR + '/jargon/terms.yml') as stream:
    TERMS = yaml.safe_load(stream)
