from django.db import models


# Create your models here.

class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    message = models.TextField(null=False)
