from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from video.apis.youtube import youtube_search

from video.forms import VideoAddForm

__all__ = ['search']


def search(request):
    context = {}

    keyword = request.GET.get('keyword')
    page_token = request.GET.get('page_token')

    if not keyword:
        return render(request, 'video/search.html', context)

    response = youtube_search(keyword, page_token)

    context['keyword'] = keyword
    context['response'] = response

    # form_list = []
    # for item in response['items']:
    #     print(item['kind'])
    #     print(item['id'])
    #
    #     form = VideoAddForm(
    #         initial={'kind': item['kind'],
    #                  'key': item['id'],
    #                  'title': item['snippet']['title'],
    #                  'desc': item['snippet']['description'],
    #                  'published_date': parse_datetime(
    #                      item['snippet']['publishedAt']),
    #                  'thumbnail': item['snippet']['thumbnails']['medium']['url'],
    #                  })
    #
    #     form_list.append(form)
    #
    # context['form_list'] = form_list

    return render(request, 'video/search.html', context)

