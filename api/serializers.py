from rest_framework import serializers

from core.models import User, Organization
from core.models import Resource, Tag
from projects.models import Project, Nomination, Claim


# from drf_haystack.serializers import HaystackSerializer
# from drf_haystack.viewsets import HaystackViewSet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        exclude = []


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        exclude = []


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


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag