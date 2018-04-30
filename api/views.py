from rest_framework import viewsets

import api.serializers as serializers
from core.models import User, Organization
from projects.models import Project, Nomination, Claim


class UserViewSet(viewsets.ModelViewSet):
    # TODO: status
    queryset = User.objects.all()  # exclude(status='Deleted')
    serializer_class = serializers.UserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    # TODO: status
    queryset = Organization.objects.all()  # .exclude(status='Deleted')
    serializer_class = serializers.OrganizationSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.exclude(status='Deleted')
    serializer_class = serializers.ProjectSerializer


class NominationViewSet(viewsets.ModelViewSet):
    queryset = Nomination.objects.exclude(deleted=True)
    serializer_class = serializers.NominationSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.exclude(deleted=True)
    serializer_class = serializers.ClaimSerializer
