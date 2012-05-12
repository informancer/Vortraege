"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from lxml import etree
from xml_compare import xml_compare

from vortraege.models import Talk

from datetime import datetime
from  django.utils.timezone import make_aware, get_default_timezone

import sys
from django.core.urlresolvers import reverse

class AllTestCase(TestCase):
    fixtures =  ['vortraege_views_testdata.json']

    def test_index(self):
        response = self.client.get(reverse('vortraege_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('talks_list' in response.context)
        self.assertEqual([talk.pk for talk in response.context['talks_list']], [1])

    def test_details(self):
        response = self.client.get(reverse('vortraege_details', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)

        # Ensure an inexistant talk throws a 404
        response = self.client.get(reverse('vortraege_details', kwargs={'talk_id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_vevent(self):
        response = self.client.get(reverse('vortraege_ical', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)

        # Ensure an inexistant talk throws a 404
        response = self.client.get(reverse('vortraege_ical', kwargs={'talk_id': 2}))
        self.assertEqual(response.status_code, 404)
        
    def test_pressetext_attachment(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_pressetext', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        for line in response.content.split('\n'):
            self.assertTrue(len(line) <= 80, 'The content should be wrapped at 80 characters')
        
    def test_aushang(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_pdf_aushang', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_aushang_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_svg_aushang', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

        with file('test/vortraege_views_testdata_aushang_1.svg') as expect_file:
            expected = etree.fromstring(expect_file.read())
            actual = etree.fromstring(response.content)        
            self.assertTrue(xml_compare(expected, actual, reporter=sys.stderr.write))

    def test_flyer(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_pdf_flyer', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

    def test_flyer_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_svg_flyer', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

