from django.shortcuts import redirect, render, get_object_or_404
from video.models import Category, Video
from video.forms import CateForm

__all__ = ['main_list', 'cate_new']


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

