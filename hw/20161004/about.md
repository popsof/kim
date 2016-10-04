$ django-admin startproject mysite
```
- mysite/: project root directory 이름은 중요치 않음
- manage.py: project를 관리하는 command line util
- mysite/: project의 실제 python package이름
- mysite/__init__.py: python package임을 알리는 file
- mysite/settings.py: 각종 setting/configuration값 관리
- mysite/urls.py: url->python program mapper
- mysite/wsgi: 나중에 자세히 알아봅시다.

```
$ python manage.py runserver
```
test밑 개발용 web server 띄우기 절대 서비스용으로 사용하지 말것

```
$ python manage.py startapp polls
```
project에 app(일종의 기능) 추가하기
