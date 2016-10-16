from django.conf.urls import url
from . import views

app_name = 'video'

urlpatterns = [
	url(r'^(\d*)$', views.main_list, name='main_list' ),
	url(r'^cate/$', views.cate_list, name='cate_list' ),
	url(r'^cate_new/$', views.cate_new, name='cate_new' ),
	url(r'^cate_edit/(\d+)/$', views.cate_edit, name='cate_edit' ),
	url(r'^video/(\d+)/$', views.video_list, name='video_list' ),
	url(r'^video_new/(\d+)/$', views.video_new, name='video_new' ),
	url(r'^video_edit/(\d+)/$', views.video_edit, name='video_edit' ),
]

