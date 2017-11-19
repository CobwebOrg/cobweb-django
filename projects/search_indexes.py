from haystack import indexes

from projects.models import Project, Nomination


class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Project

class NominationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    class Meta:
        model = Nomination