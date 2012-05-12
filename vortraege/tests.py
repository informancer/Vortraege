"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from lxml import etree
from xml_compare import xml_compare

from vortraege.models import Vortrag

from datetime import datetime
from  django.utils.timezone import make_aware, get_default_timezone

import sys

class AllTestCase(TestCase):
    def setUp(self):
        # save a dummy vortrag
        start_date = make_aware(datetime(2012, 05, 06, 16, 03, 00), get_default_timezone())
        self.vortrag = Vortrag.objects.create(datum=start_date,
                                             thema='Cooles Vortrag',
                                             referent='John Doe',
                                             orgapate='Paul Smith',
                                             beschreibung="""
This is a very nice talk, presented by a guy who really knows what he is talking about. 
The previous line should be wrapped in the text.
""")
        self.c = Client()

    def test_index(self):
        response = self.client.get('/vortraege/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vortraege_list' in response.context)
        self.assertEqual([vortrag.pk for vortrag in response.context['vortraege_list']], [1])
        
    def test_pressetext_attachment(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get('/vortraege/%i/pressetext/'%self.vortrag.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))

    def test_pressetext_wrapping(self):
        response=self.client.get('/vortraege/%i/pressetext/'%self.vortrag.pk)
        for line in response.content.split('\n'):
            self.assertTrue(len(line) <= 80, 'The content should be wrapped at 80 characters')
        
    def test_aushang(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get('/vortraege/%i/aushang/'%self.vortrag.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_aushang_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get('/vortraege/%i/aushang/preview/'%self.vortrag.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

        with file('test/expected_aushang.svg') as expect_file:
            expected = etree.fromstring(expect_file.read())
            actual = etree.fromstring(response.content)        
            self.assertTrue(xml_compare(expected, actual, reporter=sys.stderr.write))

        # The following is used to create an expected file
        #expected = open('test/expected_aushang.svg', 'w')
        #expected.write(response.content)

    def test_flyer(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get('/vortraege/%i/flyer/'%self.vortrag.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_flyer_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get('/vortraege/%i/flyer/preview/'%self.vortrag.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

