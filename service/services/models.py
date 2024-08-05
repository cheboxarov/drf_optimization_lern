from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name="subscriptions", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.company_name} - {self.service.name} ({self.plan.plan_type})"

