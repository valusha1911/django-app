from django.db import models
from absUser.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    users = models.ManyToManyField(User)
    technologies = models.ManyToManyField('Technology',
                                          related_name='projects'
                                          )

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
