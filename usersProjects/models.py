from django.db import models
from absUser.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='projects')
    technologies = models.ManyToManyField('Technology',
                                          related_name='projects'
                                          )

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Like(models.Model):
    users_id = models.ManyToManyField(User, related_name='users_id')
    projects_id = models.ManyToManyField('Project', related_name='projects_id')
