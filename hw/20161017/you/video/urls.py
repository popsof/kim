from django.conf.urls import url
from . import views

app_name = 'video'

urlpatterns = [
	url(r'^(\d*)$', views.main_list, name='main_list' ),
	url(r'^cate/new/$', views.cate_new, name='cate_new' ),
	url(r'^video/search/$', views.search, name='search' ),
	url(r'^video/add/$', views.video_add, name='video_add' ),
	url(r'^video/edit/(\d+)/$', views.video_edit, name='video_edit' ),
]

