import codecs

from django.test import Client
from django.core.urlresolvers import reverse

from django.core.management.base import BaseCommand, CommandError
from vortraege.models import Talk
#from vortraege.views import render_svg_poster, render_svg_flyer

from django.db import (transaction, connection, connections, DEFAULT_DB_ALIAS,
    reset_queries)
from django.core.management import call_command



class Command(BaseCommand):
    args = '<fixture>'
    help = 'Creates the different files for a given fixture'
    
    def handle(self, *args, **options):
        # First, load the fixture:
        db = DEFAULT_DB_ALIAS 
        call_command('flush', verbosity=0, interactive=False, database=db)
        call_command('loaddata', *args, **{'verbosity': 0,  'database': db})
        prefix = 'test/%s'%args[0].rstrip('.json')

        client = Client()

        # Then create reference svgs for all Vortraege
        for talk in Talk.objects.all():
            expected = open('%s_poster_%s.svg'%(prefix, talk.pk), 'w')
            response=client.get(reverse('vortraege_svg_poster', kwargs={'pk': 1}))
            expected.write(response.content)
            
            expected = open('%s_flyer_%s.svg'%(prefix, talk.pk), 'w')
            response=client.get(reverse('vortraege_svg_flyer', kwargs={'pk': 1}))
            expected.write(response.content)
            

