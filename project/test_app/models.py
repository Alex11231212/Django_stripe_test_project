from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=[('usd', 'USD'),
                                                       ('rub', 'RUB')])

    def __str__(self):
        return self.name
