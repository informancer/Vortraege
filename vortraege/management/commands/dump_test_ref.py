import codecs

from django.core.management.base import BaseCommand, CommandError
from vortraege.models import Vortrag
from vortraege.views import render_svg_aushang

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

        # Then create reference svgs for all Vortraege
        for v in Vortrag.objects.all():
            prefix = 'test/%s'%args[0].rstrip('.json')
            expected = codecs.open('%s_aushang_%s.svg'%(prefix, v.pk), 'w', 'utf-8')
            expected.write(render_svg_aushang(v))


