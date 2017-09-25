from django.db import models


class APIProtocol(models.Model):
    name = models.CharField(max_length=200, unique=True)
    identifier = models.URLField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.name or 'APIProtocol {}'.format(self.pk)

class APIEndpoint(models.Model):
    location = models.URLField(max_length=200, unique=True)
    organization = models.ForeignKey('core.Organization')
    protocol = models.ForeignKey(APIProtocol)

    def __str__(self):
        return self.location or 'APIEndpoint {}'.format(self.pk)