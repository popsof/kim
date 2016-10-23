from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from django.contrib.auth import authenticate as auth_auth
from django.contrib.auth import login as auth_login

from member.apis import facebook

__all__ = [
    'login',
    'login_facebook',
]


def login(request):
    context = {
        'facebook_app_id':settings.FACEBOOK_APP_ID,
    }

    if request.method != 'POST':
        messages.debug(request, 'Debug message.')
        messages.info(request, 'Info message.')
        messages.success(request, 'Success message.')
        messages.warning(request, 'Warning message.')
        messages.error(request, 'Error message.')

        return render(request, 'member/login.html', context)

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        messages.error(request, 'username and password are required.')
        return render(request, 'member/login.html', context)

    user = auth_auth(username=username, password=password)

    if user is not None:
        auth_login(request, user)
        messages.success(request, '로그인에 성공하였습니다.')
        next = request.GET.get('next')
        return redirect(next)
    else:
        messages.error(request, '로그인에 실패하였습니다.')
        return render(request, 'member/login.html', context)


def login_facebook(request):
    if request.GET.get('error'):
        messages.error(request, '페이스북 로그인을 취소하였습니다.')
        return redirect('member:login')

    if not request.GET.get('code'):
        messages.error(request, '페이스북 로그인에 실패하였습니다.')
        return redirect('member:login')

    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(request.path)

    # print(code)
    # print(request.build_absolute_uri(request.path))

    access_token = facebook.get_access_token(code, redirect_uri)
    user_id = facebook.get_user_id_from_token(access_token)
    user_info = facebook.get_user_info(user_id, access_token)

    print(user_info)
    user = auth_auth(user_info=user_info)

    if user is None:
        messages.error(request, '페이스북 로그인에 실패하였습니다.')
        return redirect('member:login')

    auth_login(request, user)
    messages.success(request, '페이스북 로그인에 성공하였습니다.')
    return redirect('video:main_list', '')
    

