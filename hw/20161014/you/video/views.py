import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Video
from .forms import CateForm, VideoForm

# Create your views here.

def main_list(request, cate_id ):
	cate_list = Category.objects.order_by( 'name' )
	if cate_id is '':
		cate_id = 0
	else:
		cate_id = int(cate_id)

	if cate_id == 0:
		video_list = Video.objects.order_by( '-created_date' ) 
	else:
		cate = get_object_or_404( Category, pk=cate_id )
		video_list = cate.video_set.order_by( '-created_date' )

	context = {
		'cur_id': cate_id,
		'cate_list': cate_list,
		'video_list': video_list,
	}
	return render( request, 'video/index.html', context )


def cate_list(request):
	cate_list = Category.objects.order_by( 'name' )
	context = {
		'cate_list': cate_list,
	}
	return render( request, 'cate/cate_list.html', context )

def cate_new(request):
	context = {
		'sub_title': 'New category',
	}

	if request.method != 'POST':
		form = CateForm()
		context['form'] = form
		return render( request, 'cate/cate_edit.html', context )

	form = CateForm(request.POST)
	if not form.is_valid():
		context['form'] = form
		return render( request, 'cate/cate_edit.html', context )

	category = form.save()
	return redirect( 'video:cate_list' )

def cate_edit(request, cate_id ):
	cate = get_object_or_404( Category, pk=cate_id )

	context = {
		'sub_title': 'Edit Category',
	}

	if request.method != 'POST':
		form = CateForm( instance=cate )
		context['form'] = form
		return render( request, 'cate/cate_edit.html', context )

	form = CateForm( request.POST, instance=cate )
	if not form.is_valid():
		context['form'] = form
		return render( request, 'cate/cate_edit.html', context )
	
	form.save()
	return redirect( 'video:cate_list' )


def video_list(request, cate_id ):
	cate = get_object_or_404( Category, pk=cate_id )
	video_list = cate.video_set.order_by( '-created_date' )
	context = {
		'cate': cate,
		'video_list': video_list,
	}
	return render( request, 'video/video_list.html', context )

def get_youtube_key( url ):
	pattern = r'www\.youtube\.com/watch\?v=([-\w]+)'
	res = re.search( pattern, url )
	if res:
		return res.group(1)
	
	return None


def video_new(request, cate_id ):
	context = {
		'sub_title': 'New Video',
	}

	cate_id = int(cate_id)
	if request.method != 'POST':
		if cate_id == 0:
			form = VideoForm()
		else:
			cate = get_object_or_404( Category, pk=cate_id )
			form = VideoForm( initial={'category': cate }, )

		context['form'] = form
		return render( request, 'video/video_edit.html', context )

	form = VideoForm(request.POST)
	if not form.is_valid():
		context['form'] = form
		return render( request, 'video/video_edit.html', context )
	
	video = form.save( commit=False )
	video.key = get_youtube_key( video.url )
	if not video.key:
		context['form'] = form
		return render( request, 'video/video_edit.html', context )

	video.save()
	return redirect( 'video:main_list', video.category.id )


def video_edit(request, video_id ):
	video = get_object_or_404( Video, pk=video_id )
	cate = video.category

	context = {
		'sub_title': 'Edit Video',
		'key': video.key,
	}

	if request.method != 'POST':
		form = VideoForm( instance=video )
		context['form'] = form
		return render( request, 'video/video_edit.html', context )

	form = VideoForm(request.POST, instance=video)
	if not form.is_valid():
		context['form'] = form
		return render( request, 'video/video_edit.html', context )

	video = form.save( commit=False )
	video.key = get_youtube_key( video.url )
	if not video.key:
		context['form'] = form
		return render( request, 'video/video_edit.html', context )

	video.save()
	return redirect( 'video:main_list', video.category.id )


