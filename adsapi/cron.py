from .models import Product
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


def DeleteExpiredProductsCronJob():
    # Delete expired products
    now = timezone.now()
    expired_products = Product.objects.filter(expiry_date__lte=now)
    expired_products.delete()

DeleteExpiredProductsCronJob()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(DeleteExpiredProductsCronJob, 'interval', minutes=1)
    scheduler.start()