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
            for template, content_type in ((template, content_type) 
                                           for template in ['poster', 'flyer'] 
                                           for content_type in ['svg', 'pdf']):
                expected = open('%s_%s_%s.%s'%(prefix, template, talk.pk, content_type), 'w')
                response=client.get(reverse('vortraege_%s_%s'%(content_type, template), 
                                            kwargs={'pk': 1}))
                expected.write(response.content)

            

