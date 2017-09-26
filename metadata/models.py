from django.db import models

# Create your models here.

class Keyword(models.Model):
	name = models.CharField(max_length=25, null=False, blank=False, unique=True)

	def __str__(self):
		return self.name

