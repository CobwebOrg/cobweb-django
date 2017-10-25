from haystack import indexes

from core.models import User, Organization


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    
    class Meta:
        model = User

class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    
    class Meta:
        model = Organization