from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#from oauth2client.tools import argparser

from video.models import Video

DEVELOPER_KEY = "AIzaSyDQFKJ4NDJKZhRw2qCxF4JfZOqlMvlHGOQ"
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

    search_res = youtube.search().list(
        q=keyword,
        part="id,snippet",
        type="video",
        maxResults=max_results,
        pageToken=page_token
    ).execute()

    id_list = [item['id']['videoId'] for item in search_res['items']]

    video_res = youtube.videos().list(
        part="id,snippet,contentDetails,statistics",
        id=",".join(id_list),
    ).execute()

    id_list = [item['id'] for item in video_res['items']]
    video_list = Video.objects.filter(key__in=id_list)
    youtube_id_list = [video.key for video in video_list]
    for item in video_res['items']:
        if item['id'] in youtube_id_list:
            item['exist'] = True

    video_res['prevPageToken'] = search_res.get('prevPageToken')
    video_res['nextPageToken'] = search_res.get('nextPageToken')

    return video_res

