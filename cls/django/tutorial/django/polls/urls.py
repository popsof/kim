from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<q_id>\d+)/$', views.detail, name='detail' ),
	url(r'^(?P<q_id>\d+)/results/$', views.results, name="results" ),
	url(r'^(?P<q_id>\d+)/vote/$', views.vote, name="vote" ),
	url(r'^(?P<q_id>\d+)/add_choice/$', views.add_choice, name="add_choice" ),
]


