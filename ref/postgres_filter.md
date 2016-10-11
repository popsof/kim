### django query
#### 참 희한한 query

```
>>> b1 = Blog.objects.create( name="b1 name", tagline="b1 tagline" )
>>> e1 = Entry.objects.create( blog=b1, headline="fast", rating = 0 )
>>> e2 = Entry.objects.create( blog=b1, headline="slow", rating = 100 )

>>> Blog.objects.filter( entry__headline__contains="fast",처 entry__rating=100 )
<QuerySet []>
>>> Blog.objects.filter( entry__headline__contains="fast").filter( entry__rating=100 )
<QuerySet [<Blog: b1 name>]>
>>> 
```
흠.. 뭐 대충 이해된다.

그럼 sql로는?? 참고로 postgres
```
SELECT blog.id, blog.name, blog.tagline FROM blog
INNER JOIN entry ON (blog.id = entry.blog_id)
WHERE (entry.headline::text LIKE '%fast%' AND entry.rating = 100) LIMIT 21
```
첫번째 query는 일반적인 1:n관계에서 n:table의 field를 조건으로 select하는 많이 본듯한 query문이다.


```
SELECT blog.id, blog.name, blog.tagline FROM blog
INNER JOIN entry ON (blog.id = entry.blog_id)
INNER JOIN entry T3 ON (blog.id = T3.blog_id)
WHERE (entry.headline::text LIKE '%fast%' AND T3.rating = 100) LIMIT 21
```
그러나.. 그러나.. 두번째 django에서 생성한 query는 이런것도 되나 싶은.. blog table에서 n에 해당하는 entry table과 join을 무려 두번이나 한다. 두번째 join할때는 table명을 구분하기 위해서 T3라는 aliasing까지 해주는 모습.(terminator 3인줄..) 각각의 join에 두가지 조건 (즉 "fast"라는 문자열이 포함된, rating이 100인) 을 따로 조건문을 만들어주면 마치 순차적으로 query해준 결과가 나오는건 이번에 처음 알았다.

대단하다 장고.
끝.
