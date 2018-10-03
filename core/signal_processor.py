from django.db import models
from haystack import signals

from core.models import User, Organization, Resource
from projects.models import Project, Nomination, Claim
from webarchives.models import ImportedRecord

# from core.search_indexes import UserIndex, OrganizationIndex, ResourceIndex
# from projects.search_indexes import ProjectIndex


MAPPING = {
    User: [None, 'organization'],
    Organization: [None],
    # Resource: [Resource],  # don't think I'm storing anything there
    Project: [None],
    Nomination: [None, 'project', 'resource'],
    Claim: [
        'nomination.project',
        'nomination.resource',
        'organization',
        'nomination',
    ],
    # ImportedRecord: [Resource],  # makes the sync take too long: do it manually after
}



class CobwebSignalProcessor(signals.BaseSignalProcessor):

    def setup(self):
        for sender in MAPPING:
            models.signals.post_save.connect(self.handle_save, sender=sender)
            models.signals.post_delete.connect(self.handle_delete, sender=sender)

    def teardown(self):
        for sender in MAPPING:
            models.signals.post_save.disconnect(self.handle_save, sender=sender)
            models.signals.post_delete.disconnect(self.handle_delete, sender=sender)



    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """

        for index_relation in MAPPING[sender]:
            if index_relation is None:
                super().handle_save(sender, instance, **kwargs)
            else:
                related = instance
                for attr_name in index_relation.split('.'):
                    related = getattr(related, attr_name)
                super().handle_save(type(related), related, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        delete should be sent to & delete the object on those backends.
        """


        for index_relation in MAPPING[sender]:
            if index_relation is None:
                super().handle_delete(sender, instance, **kwargs)
            else:
                related = instance
                for attr_name in index_relation.split('.'):
                    related = getattr(related, attr_name)
                super().handle_save(type(related), related, **kwargs)
