from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.summary),
    url(r'^summary/', views.summary, name='summary'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^api/overall_summary_half_hour',views.overall_summary_half_hour,name='overall_summary_half_hour'),
    url(r'^api/user_summary_half_hour',views.user_summary_half_hour,name='user_summary_half_hour')
]
