from haystack import indexes

from archives.models import Collection, Claim, Holding


class CollectionIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    
    class Meta:
        model = Collection

class ClaimIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    
    class Meta:
        model = Claim

class HoldingIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    
    class Meta:
        model = Holding