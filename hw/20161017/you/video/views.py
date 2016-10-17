from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from .models import Category, Video
from .forms import CateForm, VideoForm, VideoAddForm

DEVELOPER_KEY = "AIzaSyDiarbwPOxSkXmNPfdv8UtHcZM6KySpk34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(keyword, page_token, max_results=5):
    """
    youtube_search함수 개선

    1. youtube_search 함수의 arguments에 pageToken 추가
    2. 받은 pageToken값을 youtube.search()실행 시 list의 인자로 추가
    3. search뷰에서 request.GET에 pageToken값을 받아오도록 설정
    4. template에서 이전페이지/다음페이지 a태그 href에 GET parameter가 추가되도록 설정
    """
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
		type="video",
        maxResults=max_results,
        pageToken=page_token
    ).execute()

    return search_response

def main_list(request, cate_id):
	cate_list = Category.objects.order_by('name')
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
	return redirect( 'video:main_list' '' )


def search(request):

	context = {}

	keyword = request.GET.get('keyword')
	page_token = request.GET.get('page_token')

	if not keyword:
		return render(request, 'video/search.html', context)

	response = youtube_search( keyword, page_token )

	context['keyword'] = keyword
	context['response'] = response

	form_list = []
	for item in response['items']:
		print( item['kind'] )
		print( item['id']['kind'] )
		print( item['id']['videoId'] )

		form = VideoAddForm(
			initial={ 'kind': item['id']['kind'], 
					'key': item['id']['videoId'],
					'title': item['snippet']['title'],
					'desc': item['snippet']['description'],
					'published_date': parse_datetime(
										item['snippet']['publishedAt'] ),
					'thumbnail': item['snippet']['thumbnails']['medium']['url'],
					} )

		form_list.append( form )
	
	context['form_list'] = form_list

	return render(request, 'video/search.html', context)


def video_add(request):
	if request.method != 'POST':
		return redirect( 'video:search' )

	# 훗. pk=1 이라니
	cate = get_object_or_404( Category, pk=1 )

	next = request.POST.get( 'next' )
	form = VideoAddForm(request.POST)

	if not form.is_valid():
		print( 'form invalid' )
		print( form )
		return redirect(next)
	
	video = form.save(commit=False)	
	video.category = cate
	video.save()

	return redirect(next)


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
	video.save()

	return redirect( 'video:main_list', video.category.id )


