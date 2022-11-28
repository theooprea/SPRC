from django.db import models
from ..countries.models import Country

class City(models.Model):
    id_tara = models.ForeignKey(Country, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    nume_oras = models.CharField(max_length=200)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    def __str__(self):
        return self.nume_oras

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('id_tara', 'nume_oras',)
