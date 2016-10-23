from django.contrib import messages
from django.shortcuts import redirect
from sns.models import FaceRanking, FaceFriend

__all__ = [
    'save_friends',
    ]

def save_friends(request):
    if request.method != 'POST':
        return redirect('sns:index', '')

    friend_count = request.POST.get('friend_count')
    if not friend_count:
        messages.error(request, 'missing field friend_count')
        return redirect('sns:index', '')

    friend_count = int(friend_count)
    new_rank = FaceRanking.objects.create(comment="...")
    for i in range(friend_count):
        field_id = 'id_{:02d}'.format(i)
        field_name = 'name_{:02d}'.format(i)
        field_score = 'score_{:02d}'.format(i)

        value_id = request.POST.get(field_id)
        value_name = request.POST.get(field_name)
        value_score = request.POST.get(field_score)

        new_friend = FaceFriend.objects.create(
                face_ranking=new_rank,
                face_id=value_id,
                face_name=value_name,
                score=int(value_score) )

    return redirect('sns:index', '')
