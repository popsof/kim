from django.shortcuts import render, render_to_response
from .models import Post

def post_list( request ):
    posts = Post.objects.all()

    ret = {
        'title': '블로그 글 목록',
        'posts': posts
    }

    return render_to_response( 'post_list.html', ret )

    # return render( request, 'post_list.html' )

