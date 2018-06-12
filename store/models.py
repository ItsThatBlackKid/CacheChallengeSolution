from django.db import models




class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    message = models.TextField(null=False)
