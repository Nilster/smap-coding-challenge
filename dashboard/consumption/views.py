# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from consumption.models import User, Usage
from django.db.models import Sum, Avg, DecimalField
from django.http import JsonResponse
# Create your views here.


def summary(request):
    context = {
        'all_users': User.objects.values() \
                            .annotate(total_usage=Sum('usage__consumption')) \
                            .order_by('user_id'),
    }
    return render(request, 'consumption/summary.html', context)


def detail(request):
    context = {
        'all_users': User.objects.values() \
                            .annotate(total_usage=Sum('usage__consumption')) \
                            .order_by('user_id'),
    }
    return render(request, 'consumption/detail.html', context)

#Returns total consumption and average consumption for all users at half an hour time interval
def overall_summary_half_hour(request):
    all_summary = Usage.objects.values('timestamp') \
                        .annotate(total_usage=Sum('consumption'), \
                                    avg_usage=Avg('consumption',output_field=DecimalField(max_digits=10, decimal_places=1))) \
                        .order_by('timestamp')
    return JsonResponse(list(all_summary), safe=False)

#Returns user specific consumption data
def user_summary_half_hour(request):
    requested_user = request.GET['user_id']
    user_summary = Usage.objects \
                    .values('user_id','consumption','timestamp') \
                    .filter(user_id=requested_user).order_by('timestamp')
    return JsonResponse(list(user_summary), safe=False)