import time
import datetime
import json
import requests

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect, render

from member.apis import facebook


__all__ = [
    'friends_ranking',
]


def friends_ranking(request):
    if request.GET.get('error'):
        messages.success(request, '페이스북 친구확인을 취소하셨습니다.')
        return redirect('sns:index', '')

    if not request.GET.get('code'):
        messages.error(request, '페이스북 로그인에 실패하였습니다.')
        return redirect('sns:index', '')

    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(request.path)

    access_token = facebook.get_access_token(code, redirect_uri)
    if not access_token:
        messages.info(request, '페이스북 로그인이 만료되었습니다.')
        return redirect('sns:index', '')

    user_id = facebook.get_user_id_from_token(access_token)

    one_year_ago = timezone.now() - datetime.timedelta(days=365)
    since = int(time.mktime(one_year_ago.timetuple()))
#    print(since)
    
    url_user_feed = 'https://graph.facebook.com/v2.8/{}/feed' \
                    '?access_token={}' \
                    '&fields=from,comments{{from,comments}}' \
                    '&since={}'.format(
                        user_id, access_token, since )

#    print( url_user_feed )
    messages.info( request, url_user_feed )

    # 'facebook_id':count dictionary
    friends_score = {}
    friends_name = {}


#     while True :
#         r = requests.get(url_user_feed)
#         rsp_user_feed = r.json()
#
# #        json_data = json.dumps(rsp_user_feed, indent=2)
# #        print(json_data)
#
#         rsp_data0 = rsp_user_feed.get('data')
#         if not rsp_data0: break
#
#         for item0 in rsp_data0:
#             for key0,val0 in item0.items():
#                 if key0 == 'from':
#                     id = val0.get('id')
#                     if id: accum_score(friends_score, id)
#                     name = val0.get('name')
#                     if name: friends_name[id] = name
#                 elif key0 == 'comments':
#                     rsp_data1 = val0.get('data')
#                     if not rsp_data1: break
#
#                     for item1 in rsp_data1:
#                         for key1,val1 in item1.items():
#                             if key1 == 'from':
#                                 id = val1.get('id')
#                                 if id: accum_score(friends_score, id)
#                                 name = val1.get('name')
#                                 if name: friends_name[id] = name
#                             elif key1 == 'comments':
#                                 rsp_data2 = val1.get('data')
#                                 if not rsp_data2: break
#
#                                 for item2 in rsp_data2:
#                                     for key2,val2 in item2.items():
#                                         if key2 == 'from':
#                                             id = val2.get('id')
#                                             if id: accum_score(friends_score, id)
#                                             name = val2.get('name')
#                                             if name: friends_name[id] = name
#
#         rsp_paging = rsp_user_feed.get('paging')
#         if not rsp_paging:
#             break
#
#         rsp_next = rsp_paging.get('next')
#         if not rsp_next:
#             break
#
#         url_user_feed = rsp_next


    while True:
        r = requests.get(url_user_feed)
        rsp_user_feed = r.json()

        main_data = rsp_user_feed.get('data')
        if not main_data: break

        proc_data(friends_score, friends_name, main_data)

        rsp_paging = rsp_user_feed.get('paging')
        if not rsp_paging:
            break

        rsp_next = rsp_paging.get('next')
        if not rsp_next:
            break

        url_user_feed = rsp_next

    friend_list = [(id, friends_name[id], score) \
                    for id,score in friends_score.items()]
#    print(friend_list)
    friend_list = sorted(friend_list, key=lambda x: (x[2],x[1]), reverse=True)
#    print(friend_list)
    friend_list = friend_list[:50]

    context = {
        'access_token': access_token,
        'friend_list': friend_list,
        }

    return render(request, 'sns/friends_ranking.html', context)


def proc_data(friends_score, friends_name, data):
    for item in data:
        for key,val in item.items():
            if key == 'from':
                id = val.get('id')
                if id: accum_score(friends_score, id)
                name = val.get('name')
                if name: friends_name[id] = name
            elif key == 'comments':
                com_data = val.get('data')
                if not com_data: break

                proc_data(friends_score, friends_name, com_data)


def accum_score( friends_score, id ):
    score = friends_score.get(id)
    if score:
        score += 1
    else:
        score = 1

#    print( id, score )
    friends_score[id] = score

