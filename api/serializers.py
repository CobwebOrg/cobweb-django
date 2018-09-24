from languages_plus.models import Language
from rest_framework import serializers

from core.models import User, Organization
from core.models import Resource, Tag
from projects.models import Project, Nomination, Claim
from webarchives.models import ImportedRecord


# from drf_haystack.serializers import HaystackSerializer
# from drf_haystack.viewsets import HaystackViewSet


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['iso', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        exclude = []


class NominationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'name']
    
    url = serializers.URLField(source='get_absolute_url')


class NominationMDSerialier(serializers.ModelSerializer):
    """
    Serializes only a Nomination's general fields related to a resource.
    
    This excludes fields that are specific to its nomination in a given project.
    """
    class Meta:
        model = Nomination
        fields = ['title', 'author', 'language', 'description', 'tags', 'subject_headings']

    language = LanguageSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    subject_headings = TagSerializer(required=False, many=True)

    def to_representation(self, instance):
        """Wraps each value of self.data.metadata in a set."""

        data = super().to_representation(instance)
        for field in data:
            if field not in {'tags', 'subject_headings'}:
                data[field] = [data[field]]
        return data


class ResourceNominationSerializer(serializers.ModelSerializer):
    """
    Serializes only a Nomination's general fields related to a resource.

    This excludes fields that are specific to its nomination in a given project.
    """
    class Meta:
        model = Nomination
        fields = ['source', 'metadata', 'url']

    source = NominationProjectSerializer(source='project')
    metadata = NominationMDSerialier(source='*')
    url = serializers.URLField(source='get_absolute_url')


class ArchiveOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedRecord
        fields = ['url', 'name']
    
    url = serializers.URLField(source='identifier')


class ArchiveResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedRecord
        fields = ['source', 'metadata', 'url']
    
    source = ArchiveOrgSerializer(source='organization', required=True, many=False)
    url = serializers.URLField(source='get_absolute_url')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['url', 'nominations', 'imported_records']
    
    nominations = ResourceNominationSerializer(required=False, many=True)
    imported_records = ArchiveResourceSerializer(required=False, many=True)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        exclude = []


class NominationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nomination
        exclude = []


class ClaimSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Claim
        exclude = []
