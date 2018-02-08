import django.test

import core.search_indexes
from metadata.tests.factories import KeywordFactory
from projects.tests.factories import ProjectFactory


class ProjectIndexTest(django.test.TestCase):

    def test_metadata_populates_document_field(self):
        """All metadata should be in the dict returned by metadata_as_dict."""
        index = core.search_indexes.ProjectIndex()

        project = ProjectFactory(
            title='Project Name',
            metadata={'a': [1], 'b': [2, 3]}
        )
        project.save()
        project.keywords.add(KeywordFactory())
        project.keywords.add(KeywordFactory())

        solr_dict = index.prepare(project)
        solr_document = solr_dict['text']

        self.assertIn('Project Name', solr_document)
        for kw in project.keywords.all():
            self.assertIn(str(kw), solr_document)
        for key, values in project.metadata.items():
            for value in values:
                self.assertIn(str(value), solr_document)
