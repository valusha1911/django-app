from rest_framework import serializers

from absUser.models import User
from usersProjects.models import Project, Technology

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'projects', )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('url', 'id', 'title', 'description', 'users', 'technologies', )


class TechnologySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Technology
        fields = ('url', 'id', 'title', 'projects', )
