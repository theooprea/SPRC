from django.db import models
from ..cities.models import City

# Time format, as specified in the assignment, year - month - day
TIME_FORMAT = "%Y-%m-%d"

# DB Model for a Temperature, containing a float field "valoare", a
# datetime field "timestamp", which is automatically set when a new
# Temperature object is created, and a foreign key field, "id_oras",
# which points to the "id" field of the City Model.
# There is also an autoincrement "id" field inherited from models.Model
# class and a unique constraint on the pair (id_tara, nume_oras)
class Temperature(models.Model):
    valoare = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    id_oras = models.ForeignKey(City, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # used for the Admin view in Django
    def __str__(self):
        return self.id_oras.nume_oras + " - " + self.timestamp.strftime(TIME_FORMAT)

    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Temperatures"
        # unique constraint on the pair (id_oras, timestamp)
        unique_together = ('id_oras', 'timestamp',)
