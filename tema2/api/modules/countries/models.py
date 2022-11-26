from django.db import models

class Country(models.Model):
    nume_tara = models.CharField(max_length=200, unique=True)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
