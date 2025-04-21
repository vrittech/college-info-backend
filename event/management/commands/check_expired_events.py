# management/commands/check_expired_events.py
from django.core.management.base import BaseCommand
from datetime import datetime
from event.models import Event  

class Command(BaseCommand):
    help = 'Check and update expired events'

    def handle(self, *args, **kwargs):
        expired_events = Event.objects.filter(end_date__lt=datetime.now(), is_expired=False)
        
        # Update is_expired to True for all expired events
        expired_events.update(is_expired=True)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {expired_events.count()} expired events.'))
