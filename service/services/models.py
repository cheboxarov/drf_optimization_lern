from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):

        from .tasks import set_price

        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)


class Plan(models.Model):

    class PLAN_TYPES(models.TextChoices):
        FULL = 'full', "Full"
        STUDENT = 'student', 'Student'
        DISCOUNT = 'discount', "Discount"

    plan_type = models.CharField(choices=PLAN_TYPES.choices, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):

        from .tasks import set_price

        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name="subscriptions", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="subscriptions", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name="subscriptions", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.client.company_name} - {self.service.name} ({self.plan.plan_type})"
