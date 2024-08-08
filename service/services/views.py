from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from django.db.models import Prefetch
from .serializers import SubscriptionSerializer
from clients.models import Client
from django.db.models import Sum
from django.core.cache import cache
from django.conf import settings


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = (Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all()
                 .select_related('user').only('company_name', 'user__email'))))

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        queryset = self.get_queryset()

        price_cache = cache.get(settings.PRICE_CACHE_NAME)
        if price_cache:
            total_amount = price_cache
        else:
            total_amount = queryset.aggregate(total=Sum('price'))["total"]
            cache.set(settings.PRICE_CACHE_NAME, total_amount, 60*60)

        response_data = {
            'total_amount': total_amount,
            'result': response.data
        }
        response.data = response_data

        return response