from django.db import models


class Moto(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    model_name = models.CharField(max_length=2048, null=True)
    price_per_day = models.CharField(max_length=2048, null=True)
    photo = models.ImageField(null=True)
    rented = models.BooleanField(default=False)


class Yacht(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    model_name = models.CharField(max_length=2048, null=True)
    price_per_day = models.CharField(max_length=2048, null=True)
    photo = models.ImageField(null=True)
    rented = models.BooleanField(default=False)
