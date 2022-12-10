from django.db import models

# DB Model for a country, containing a char field "nume_tara",
# and 2 float fields, "latitudine" and "longitudine". There is
# also an autoincrement "id" field inherited from models.Model class
# and a unique restriction places on the "nume_tara" field
class Country(models.Model):
    nume_tara = models.CharField(max_length=200, unique=True)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    # used for the Admin view in Django
    def __str__(self):
        return self.nume_tara
    
    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Countries"
