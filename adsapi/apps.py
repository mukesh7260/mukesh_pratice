# from django.apps import AppConfig


# class AdsapiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'adsapi'



import time as mytime
from django.apps import AppConfig
import schedule
import threading
from django.core.management import call_command

# create function for calling mycronjob.py file
def my_cron_job():
    call_command('delete_expired_products')

class AdsapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adsapi'
    def ready(self):
        # Schedule the cron job to run daily at a specific time (adjust as needed)
        schedule.every().day.at("10:36").do(my_cron_job)
        # Start the scheduling loop in a separate thread
        def run_continuously():
            while True:
                schedule.run_pending()
                mytime.sleep(1)
                # print("Script running")
        # Start the scheduling loop thread
        thread = threading.Thread(target=run_continuously)
        #Daemon threads are threads that run in the background
        # and are automatically terminated when the main program (also known as the "parent" thread) exits.
        thread.daemon = True  
        thread.start() # Start the thread’s activity.




## There is one disadvatage of using the thread when we didnot use thread then he block django aplication main thread

##then server is not working