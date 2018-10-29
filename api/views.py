from rest_framework import viewsets

from absUser.models import User
from usersProjects.models import Project, Technology
from api.serializers import UserSerializer, ProjectSerializer, TechnologySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TechnologyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
