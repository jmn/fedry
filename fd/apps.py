from django.apps import AppConfig

import django_rq

class FdConfig(AppConfig):
    name = 'fd'

    def ready(self):
        import fd.signals
        import fd.services
        from datetime import datetime
        
        scheduler = django_rq.get_scheduler('default')

        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        # Have 'mytask' run every 20 minutes
        scheduler.schedule(datetime.utcnow(), 'fd.services.update_from_all_feeds', interval=60*15)
