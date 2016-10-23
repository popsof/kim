from django.shortcuts import render, get_object_or_404
from django.conf import settings

from sns.models import FaceRanking, FaceFriend


__all__ = [
    'index',
]

def index(request, rank_id):
    if rank_id is '':
        rank_id = 0
    else:
        rank_id = int(rank_id)

    if rank_id > 0:
        rank = get_object_or_404(FaceRanking, pk=rank_id)
    else:
        rank = None

    rank_list = get_rank_list(rank, 2)
    if rank_list and not rank:
        rank = rank_list[-1]
    
    if rank_list.index(rank) > 1:
        prev_rank = rank_list[rank_list.index(rank)-1]
    else:
        prev_rank = None

    friend_list = list(
            rank.facefriend_set.order_by('-score', '-face_name')[:50])
    if prev_rank:
        prev_list = list(
                prev_rank.facefriend_set.order_by('-score', '-face_name')[:50])
        make_updown( friend_list, prev_list )

    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'cur_rank': rank,
        'rank_list': rank_list,
        'friend_list': friend_list,
    }
    return render(request, 'sns/index.html', context)


def find_index(friend_list, face_id):
    for i, friend in enumerate(friend_list):
        if friend.face_id == face_id:
            return i

    return -1


def make_updown( friend_list, prev_list ):
    for i, friend in enumerate(friend_list):
        prev_index = find_index(prev_list, friend.face_id)
        if prev_index < 0:
            friend.updown = 1000
        else:
            friend.updown = prev_index - i


def get_rank_list(cur_rank=None, count_each=5):
    if not cur_rank:
        tot_count = count_each * 2 + 1
        rank_list = list(FaceRanking.objects.order_by('-created_date')[:tot_count])
        rank_list.reverse()
        return rank_list

    count_before = FaceRanking.objects.filter(
                        created_date__lt=cur_rank.created_date).count()
    count_behind = FaceRanking.objects.filter(
                        created_date__gt=cur_rank.created_date).count()

    print(count_each,count_before,count_behind)
    if count_before < count_each:
        count_behind = min(count_behind, count_each * 2 - count_before)
    elif count_behind < count_each:
        count_before = min(count_before, count_each * 2 - count_behind)
    else:
        count_before = min(count_before, count_each)
        count_behind = min(count_behind, count_each)

    print(count_each,count_before,count_behind)

    rank_list = [cur_rank]

    if count_before > 0:
        before_list = FaceRanking.objects.\
                    filter(created_date__lt=cur_rank.created_date).\
                    order_by('-created_date')[:count_before]
        before_list = list(before_list)
        before_list.reverse()
        rank_list = before_list + rank_list

    if count_behind > 0:
        behind_list = FaceRanking.objects.\
                    filter(created_date__gt=cur_rank.created_date).\
                    order_by('created_date')[:count_behind]
        behind_list = list(behind_list)
        rank_list = rank_list + behind_list

    return rank_list

