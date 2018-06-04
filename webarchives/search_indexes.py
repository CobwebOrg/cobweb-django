from haystack import indexes

from webarchives.models import ImportedRecord, APIEndpoint


# class ImportedRecordIndex(indexes.ModelSearchIndex, indexes.Indexable):

#     name = indexes.CharField(model_attr='name', indexed=True, stored=True)
#     text = indexes.CharField(document=True, use_template=False)

#     class Meta:
#         model = ImportedRecord


# class APIEndpointIndex(indexes.ModelSearchIndex, indexes.Indexable):

#     name = indexes.CharField(model_attr='name', indexed=True, stored=True)
#     text = indexes.CharField(document=True, use_template=False)

#     class Meta:
#         model = APIEndpoint
