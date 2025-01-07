from django.core.management.base import BaseCommand
from adsapi.models import Product
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete expired products'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_products = Product.objects.filter(expiry_date__lte=now)
        expired_products.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted expired products'))
