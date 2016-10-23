from django.conf.urls import url
from . import views

app_name = 'sns'
urlpatterns = [
    url(r'^(\d*)$', views.index, name='index'),
    url(r'^facebook/friends_ranking/$', views.friends_ranking, name='friends_ranking'),
    url(r'^facebook/save_friends/$', views.save_friends, name='save_friends'),
]
