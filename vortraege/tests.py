"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from vortraege.models import Vortrag

from datetime import datetime
from django.utils.timezone import utc, now

class AllTestCase(TestCase):
    def setUp(self):
        # save a dummy vortrag
        self.vortrag = Vortrag.objects.create(datum=now(),
                                             thema='Cooles Vortrag',
                                             referent='John Doe',
                                             orgapate='Paul Smith',
                                             beschreibung="""
This is a very nice talk, presented by a guy who really knows what he is talking about. 
The previous line should be wrapped in the text.
""")
        self.c = Client()
                                             
    def test_pressetext_attachment(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.c.get('/vortraege/%i/pressetext/'%self.vortrag.pk)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))

    def test_pressetext_wrapping(self):
        response=self.c.get('/vortraege/%i/pressetext/'%self.vortrag.pk)
        for line in response.content.split('\n'):
            self.assertTrue(len(line) <= 80, 'The content should be wrapped at 80 characters')
        
    def test_aushang(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.c.get('/vortraege/%i/aushang/'%self.vortrag.pk)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_aushang_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.c.get('/vortraege/%i/aushang/preview/'%self.vortrag.pk)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

    def test_flyer(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.c.get('/vortraege/%i/flyer/'%self.vortrag.pk)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_flyer_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.c.get('/vortraege/%i/flyer/preview/'%self.vortrag.pk)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

