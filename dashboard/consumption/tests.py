# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from consumption.models import User, Usage
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum, Avg, DecimalField


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
        Usage.objects.create(user_id=test_user,timestamp=timezone.now(), consumption=111, filename=r'C:\test.csv')

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
        current_t = timezone.now()
        for user_num in range(15):
            user = User.objects.create(user_id=user_num,area='a'+str(user_num),tariff='t'+str(user_num))
            for i in reversed(range(10)):
                #oldest time would have highest usage
                usage_t = current_t - timezone.timedelta(minutes=(30*i)) 
                usage = Usage.objects.create(user_id=user, \
                                            timestamp=usage_t, \
                                            consumption=i*10, \
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

    #Some additional tests for annotation
    def test_summary_total_annotation(self):
        user_summary = User.objects.annotate(total_usage=Sum('usage__consumption')).order_by('user_id')
        #For any user the total consumption would be 450 
        self.assertEqual(user_summary.first().total_usage, 450)

    def test_summary_timed_total(self):
        #For the oldest time, total consumption for all the users would be 90*15
        total_summary = Usage.objects.values('timestamp') \
                                .annotate(total_usage=Sum('consumption'), \
                                          avg_usage=Avg('consumption',output_field=DecimalField(max_digits=10, decimal_places=1))) \
                                .order_by('timestamp')
        oldest_total_usage = total_summary[0]['total_usage']
        self.assertEqual(oldest_total_usage, 1350)