import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clients.models import Client
from services.models import Service, Subscription, Plan

class Command(BaseCommand):
    help = 'Populate the database with 1000 clients and subscriptions'

    def handle(self, *args, **kwargs):
        # Create 1000 users and clients
        for i in range(1000):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='password',
                    email=f'user{i}@example.com'
                )
                Client.objects.create(
                    user=user,
                    company_name=f'Company {i}',
                    full_address=f'Address {i}'
                )

        # Create some services
        services = [
            Service.objects.create(name=f'Service {i}', full_price=random.randint(100, 1000))
            for i in range(10)
        ]

        # Create some plans
        plans = [
            Plan.objects.create(plan_type=random.choice(['full', 'student', 'discount']), discount_percent=random.randint(0, 100))
            for _ in range(3)
        ]

        # Create 1000 subscriptions
        clients = Client.objects.all()
        for client in clients:
            service = random.choice(services)
            plan = random.choice(plans)
            Subscription.objects.create(
                client=client,
                service=service,
                plan=plan
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
