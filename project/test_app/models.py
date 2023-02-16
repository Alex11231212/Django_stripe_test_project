from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=[('usd', 'USD'),
                                                       ('rub', 'RUB')])

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent = models.IntegerField()
    factor = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.factor = 1 - (self.percent / 100)
        super().save()

    def __str__(self):
        return str(self.percent)


class Tax(models.Model):
    percent = models.IntegerField()
    factor = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    country = models.CharField(max_length=2, choices=[('ru', 'Russia'),
                                                      ('us', 'USA')])

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.factor = 1 + (self.percent / 100)
        super().save()

    def __str__(self):
        return str(self.percent)


class Order(models.Model):
    item = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, default=0,
                                 on_delete=models.SET_DEFAULT)
    tax = models.ForeignKey(Tax, default=0,
                            on_delete=models.SET_DEFAULT)

    @property
    def get_net_price(self):
        queryset = self.item.all().aggregate(
            net_price=models.Sum('price')
        )
        return queryset['net_price']

    @property
    def get_discounted_price(self):
        discounted_price = self.get_net_price * self.discount.factor
        return discounted_price

    @property
    def get_total_price(self):
        total_price = self.get_net_price * self.discount.factor * self.tax.factor
        return round(total_price, 2)