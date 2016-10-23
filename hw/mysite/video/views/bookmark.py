from django.shortcuts import redirect, render, get_object_or_404
from video.models import Category, Video
from video.forms import VideoAddForm, VideoForm

__all__ = ['video_add', 'video_edit']


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


