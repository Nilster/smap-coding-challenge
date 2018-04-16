# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from consumption.models import User, Usage
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
import random

# Create your tests here.
#Test that you can create a user
class UserModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(user_id=999,area='a1',tariff='t1')

    def test_user_insert(self):
        user = User.objects.get(id=1)
        self.assertEquals('999', str(user))

#Test that you can create user and usage for that user.
#Test that user_id ForeignKey is in place
class UsageModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(user_id=991,area='a1',tariff='t1')
        Usage.objects.create(user_id=test_user,timestamp=datetime.now(), consumption=111, filename=r'C:\test.csv')

    def test_usage_insert(self):
        usage= Usage.objects.get(id=1)
        self.assertEquals('111.0', str(usage))

    #If we could query users based on usage information, it means that the FoerignKey exists
    #Ideally, test should reverse track usage based on user's info (eg.tariff, area etc) but for some reason reverse tracking is not working
    def test_usage_fk(self):
        self.assertTrue(User.objects.filter(usage__consumption = 111 ).count() > 0)

class SummaryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(15):
            user = User.objects.create(user_id=user_num,area='a'+str(user_num),tariff='t'+str(user_num))
            for consumption in range(10):
                usage = Usage.objects.create(user_id=user, \
                                            timestamp=datetime.now(tz=timezone.utc), \
                                            consumption=random.randrange(30,50), \
                                            filename=r'C:\test_%s.csv' % str(user_num) ) 

    def test_view_summary_url_exists(self):
        resp = self.client.get('/summary/')
        self.assertEqual(resp.status_code, 200)

    def test_view_summary_url_by_name(self):
        resp = self.client.get(reverse('summary'))
        self.assertEqual(resp.status_code, 200)

    def test_view_summary_uses_correct_template(self):
        resp = self.client.get(reverse('summary'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'consumption/summary.html')