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

from filecmp import cmp
from tempfile import mkstemp
from os import remove, fdopen

class AllTestCase(TestCase):
    fixtures =  ['vortraege_views_testdata.json']

    def test_index(self):
        response = self.client.get(reverse('vortraege_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('talks_list' in response.context)
        self.assertEqual([talk.pk for talk in response.context['talks_list']], [1])

    def test_details(self):
        response = self.client.get(reverse('vortraege_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        # Ensure an inexistant talk throws a 404
        response = self.client.get(reverse('vortraege_details', kwargs={'pk': 2}))
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
        
    def test_poster(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_pdf_poster', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'] == 'application/pdf')

        actual_fd, actual_filename = mkstemp()
        actual = fdopen(actual_fd, 'w')
        actual.write(response.content)
        actual.close()
        
        self.assertTrue(cmp('test/vortraege_views_testdata_poster_1.pdf', actual_filename, 
                            shallow = 0))
        remove(actual_filename)

    def test_poster_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_svg_poster', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

        with file('test/vortraege_views_testdata_poster_1.svg') as expect_file:
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

        actual_fd, actual_filename = mkstemp()
        actual = fdopen(actual_fd, 'w')
        actual.write(response.content)
        actual.close()
        
        self.assertTrue(cmp('test/vortraege_views_testdata_flyer_1.pdf', actual_filename, 
                            shallow = 0))
        remove(actual_filename)

    def test_flyer_preview(self):
        """
        Tests that the pressetext is an attachment
        """
        response=self.client.get(reverse('vortraege_svg_flyer', kwargs={'talk_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment'))
        self.assertTrue(response['Content-Type'].startswith('image/svg+xml'))

        with file('test/vortraege_views_testdata_flyer_1.svg') as expect_file:
            expected = etree.fromstring(expect_file.read())
            actual = etree.fromstring(response.content)        
            self.assertTrue(xml_compare(expected, actual, reporter=sys.stderr.write))

from vortraege.templatetags.vortraege_extra import author_and_title

class TalkStub(object):
    def __init__(self, speaker, title):
        self.speaker = speaker
        self.title = title

class TemplateTagsTestCases(TestCase):

    def test_short_title(self):
        talk = TalkStub('john doe', 'a short talk')
        actual = author_and_title(talk, '20,10,150')
        expected = '<tspan x="0" y="0">john doe</tspan><tspan x="0" y="15.000000">a short talk</tspan>'
        self.assertEqual(actual, expected, "Wrong formatting for a short title")

    def test_long_title(self):
        talk = TalkStub('john doe', 
                        'a short talk with a name way longer than needed')
        actual = author_and_title(talk, '30,10,150')
        expected = '<tspan x="0" y="0">john doe: a short talk with a</tspan><tspan x="0" y="15.000000">name way longer than needed</tspan>'
        self.assertEqual(actual, expected, "Wrong formatting for a long title")

    def test_very_long_title(self):
        talk = TalkStub('john doe', 
                        'a short talk with a name way longer than would absolutely be necessary')
        actual = author_and_title(talk, '30,10,150')
        expected = '<tspan x="0" y="0">john doe: a short talk with a</tspan><tspan x="0" y="15.000000">name way longer than would absolutely be necessary</tspan>'
        self.assertEqual(actual, expected, "Wrong formatting for a very title")

