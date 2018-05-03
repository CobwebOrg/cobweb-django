from haystack import indexes

from archives.models import Collection


class CollectionIndex(indexes.ModelSearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Collection
