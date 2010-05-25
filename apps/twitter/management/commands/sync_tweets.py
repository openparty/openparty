import sys
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.twitter.models import Tweet


class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start syncing'
        if len(args) == 1:
            if args[0] == 'all':
                sync_all = True
                query = '#openparty'
            else:
                sync_all = False
                query = args[0]
        elif len(args) == 2:
            if args[0] == 'all':
                sync_all = True
                query = args[1]
            else:
                print 'Paramerters was wrong'
                sys.exit()
        else:
            sync_all = False
            query = '#openparty'
        
        if sync_all:
            count = Tweet.objects.sync_all(query=query)
        else:
            count = Tweet.objects.sync(query=query)
        
        print 'Synced %s tweets' % count

