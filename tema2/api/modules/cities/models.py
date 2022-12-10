from django.db import models
from ..countries.models import Country

# DB Model for a City, containing a char field "nume_oras",
# 2 float fields, "latitudine" and "longitudine" and a foreign key
# field, "id_tara", which points to the "id" field of the Country Model.
# There is also an autoincrement "id" field inherited from models.Model
# class and a unique constraint on the pair (id_tara, nume_oras)
class City(models.Model):
    id_tara = models.ForeignKey(Country, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    nume_oras = models.CharField(max_length=200)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    # used for the Admin view in Django
    def __str__(self):
        return self.nume_oras

    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Cities"
        # unique constraint on the pair (id_tara, nume_oras)
        unique_together = ('id_tara', 'nume_oras',)
