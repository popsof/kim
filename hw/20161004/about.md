
### 시작하기

```
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

url을 app과 연결하기

mysite/urls.py (main)
	
	urlpatterns = [
		url(r'^polls/', include('polls.urls') ),
		url(r'^admin/', admin.site.urls),
	]
	
polls/urls.py (app)

	urlpatterns = [
		url(r'^$', views.index, name='index' ),
	]
	
main과 app의 url mapping 방식이다.


`r'^polls/'`에 match된 url은 app의 url에서 다시 match하는 방식인듯. app에서의 match는 아무것도 없는 url임으로 결국

`hostname.com/polls/` 로 접근한 요청은  `views.index`라는 함수에서 처리하겠다는 의미.

### 그럼 이제 Database

	polls/models.py
	
	class Question(models.Model):
		question_text = models.CharField(max_length=200)
		pub_date = models.DateTimeField('date published')
		
	class Choice(models.Model):
		question = models.ForeignKey(Question,on_delete=models.CASCADE)
		choice_text = models.CharField(max_length=200)
		votes = models.IntegerField(default=0)

설명이 필요없을 정도로 직관적이다.

`question`, `choice`두개의 table을 만들고 `choice`에서  `question`의 record를 참조하며(foreign key) 지워지면 같이 지워지는 방식인듯.

아래의 세단계 방식으로 모델링을 관리한다.

1. 위에서 처럼 models.py 작성
2. `python manage.py makemigrations` database migration script작성
3. `python manage.py migrate` 2번에서 만든 script적용

```
BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"choice_text" varchar(200) NOT NULL,
	"votes" integer NOT NULL
);

--
-- Create model Question
--
CREATE TABLE "polls_question" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"question_text" varchar(200) NOT NULL,
	"pub_date" datetime NOT NULL
);

--
-- Add field question to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";
CREATE TABLE "polls_choice" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"choice_text" varchar(200) NOT NULL,
	"votes" integer NOT NULL,
	"question_id" integer NOT NULL REFERENCES "polls_question" ("id")
);

INSERT INTO "polls_choice" ("votes", "question_id", "id", "choice_text")
	SELECT "votes", NULL, "id", "choice_text" FROM "polls_choice__old";

DROP TABLE "polls_choice__old";
CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
COMMIT;
```

`models.py`에 정의한 내용이 대략 이렇게 만들어진다. 장고에서 default로 제공하는 sqllite의 스키마인것 같다. 살펴보면 foreign key지정을 ALTER TABLE을 통해서 수행하며 table의 schema가 바뀔것을 가정하여(ALTER TABLE)의 영향인듯.. 새로운 테이블을 만들고 copy하는 명령이 포함되 있다.

### python shell로 한번..

`python manage.py shell`

`Question.objects.all()`
`select * from question`

`Question.objects.filter( id=1 )`
`select * from question where id = 1`

대략 이런 느낌?

### url 몇개 추가 한번..

	urlpatterns = [
		url(r'^$', views.index, name='index' ),
		url(r'^(?P<question_id>\d+)/$', views.detail, name='detail' ),
		url(r'^(?P<question_id>\d+)/results/$', views.results, name='results' ),
		url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote' ),
		
	/polls/
	/polls/5/
	/polls/5/results/
	/polls/5/vote/
	
`(?P<question_id>\d+)` 복잡해 보인다 하지만.. 원래 ()로 지정하면 나중에 match된 부분을 index로 알 수 있다. ?P<param>을 추가하면 param이라는 이름으로 match된 부분을 가져올 수 있는것.. 장고 url mapping에서는 url에서 추출한 question_id를 지정한 함수의 argument로 전달할듯..

### 그럼 template을 써서 좀..

	polls/templates/polls/index.hmtl
	
	{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
	{% else %}
    <p>No polls are available.</p>
	{% endif %}

이 역시 설명이 전혀 필요 없을 정도 html file을 위와 같이 작성하면 장고에서 html file을 return하기 전에 `{{ }}`, `{% %}` 이런 부분을 적당히 처리해준다.
	
###### 이제 당신은 장고 마스터.
	
