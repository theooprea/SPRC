from django.db import models

class Country(models.Model):
    nume_tara = models.CharField(max_length=200, unique=True)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    def __str__(self):
        return self.nume_tara
    
    class Meta:
        verbose_name_plural = "Countries"
