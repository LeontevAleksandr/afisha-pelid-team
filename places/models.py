from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    de

    def __str__(self):
        return self.name

# Create your models here.
