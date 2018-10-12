from rest_framework import viewsets

import api.serializers as serializers
from core.models import User, Organization
from core.models import Resource, Tag
from projects.models import Project, Nomination, Claim


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: status
    queryset = User.objects.all()  # exclude(status='Deleted')
    serializer_class = serializers.UserSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: status
    queryset = Organization.objects.all()  # .exclude(status='Deleted')
    serializer_class = serializers.OrganizationSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = serializers.ResourceSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.exclude(status='Deleted')
    serializer_class = serializers.ProjectSerializer


class NominationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nomination.objects.all()
    serializer_class = serializers.NominationSerializer


class ClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = serializers.ClaimSerializer
