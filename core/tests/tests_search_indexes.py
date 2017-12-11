import django.test

import core.search_indexes
import metadata.tests
import projects.tests


class ProjectIndexTest(django.test.TestCase):

    def test_metadata_populates_document_field(self):
        """All metadata should be in the dict returned by metadata_as_dict."""
        index = core.search_indexes.ProjectIndex()

        project = projects.tests.ProjectFactory(
            title='Project Name',
            metadata={'a': [1], 'b': [2, 3]}
        )
        project.save()
        project.keywords.add(metadata.tests.KeywordFactory())
        project.keywords.add(metadata.tests.KeywordFactory())

        solr_dict = index.prepare(project)
        solr_document = solr_dict['text']

        self.assertIn('Project Name', solr_document)
        for kw in project.keywords.all():
            self.assertIn(str(kw), solr_document)
        for key, values in project.metadata.items():
            for value in values:
                self.assertIn(str(value), solr_document)
