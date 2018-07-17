from django.db import models

class Session(models.Model):
    name = models.CharField(max_length=25, default='Our Nearest Place')
    code = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=50)
    place_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Location(models.Model):
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    session = models.ForeignKey(Session)