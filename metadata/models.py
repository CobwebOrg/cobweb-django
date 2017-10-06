import reversion
from django.db import models

# Create your models here.

@reversion.register()
class Keyword(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

