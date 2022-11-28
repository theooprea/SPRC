from django.db import models
from ..cities.models import City

TIME_FORMAT = "%Y-%m-%d"

class Temperature(models.Model):
    valoare = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    id_oras = models.ForeignKey(City, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id_oras.nume_oras + " - " + self.timestamp.strftime(TIME_FORMAT)

    class Meta:
        verbose_name_plural = "Temperatures"
        unique_together = ('id_oras', 'timestamp',)
