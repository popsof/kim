### postgres 사용자 권한 설정하기
#### createdb권한 주기

일단 확인
```
postgres=# \d pg_user
     View "pg_catalog.pg_user"
    Column    |  Type   | Modifiers 
--------------+---------+-----------
 usename      | name    | 
 usesysid     | oid     | 
 usecreatedb  | boolean | 
 usesuper     | boolean | 
 userepl      | boolean | 
 usebypassrls | boolean | 
 passwd       | text    | 
 valuntil     | abstime | 
 useconfig    | text[]  | 
```
이렇게 생긴 table(실제로는 view네요)로 관리합니다.

내용을 보면

```
postgres=# select * from pg_user;
 usename  | usesysid | usecreatedb | usesuper | userepl | usebypassrls |  passwd  | valuntil | useconfig 
----------+----------+-------------+----------+---------+--------------+----------+----------+-----------
 postgres |       10 | t           | t        | t       | t            | ******** |          | 
 tory     |    16385 | f           | f        | f       | f            | ******** |          | 
(2 rows)
```
두명의 user가 등록되있다. `postgres`와 `tory`(내가 등록한 user) 
view여서 조금 불안하지만 그래 update 시도
```
postgres=# update pg_user set usecreatedb='t' where usename='tory';
ERROR:  cannot update view "pg_shadow"
DETAIL:  Views that do not select from a single table or view are not automatically updatable.
HINT:  To enable updating the view, provide an INSTEAD OF UPDATE trigger or an unconditional ON UPDATE DO INSTEAD rule.

```
역시 실패. 더 문제는 `pg_shadow`도 역시 view다. 다시 추적해보면 `pg_authid`라는 table이 나온다.
```
postgres=# \d pg_authid
             Table "pg_catalog.pg_authid"
     Column     |           Type           | Modifiers 
----------------+--------------------------+-----------
 rolname        | name                     | not null
 rolsuper       | boolean                  | not null
 rolinherit     | boolean                  | not null
 rolcreaterole  | boolean                  | not null
 rolcreatedb    | boolean                  | not null
 rolcanlogin    | boolean                  | not null
 rolreplication | boolean                  | not null
 rolbypassrls   | boolean                  | not null
 rolconnlimit   | integer                  | not null
 rolpassword    | text                     | 
 rolvaliduntil  | timestamp with time zone | 
Indexes:
    "pg_authid_oid_index" UNIQUE, btree (oid), tablespace "pg_global"
    "pg_authid_rolname_index" UNIQUE, btree (rolname), tablespace "pg_global"
Tablespace: "pg_global"
```
위에 보이는 `rolcreaterole`이 database 생성 권한이다. table임으로 update문으로 변경할 수 있다.
```
postgres=# update pg_authid set rolcreatedb='t' where rolname='tory';
UPDATE 1
```
```
postgres=# select rolname, rolsuper, rolcreatedb from pg_authid;
 rolname  | rolsuper | rolcreatedb 
----------+----------+-------------
 postgres | t        | t
 tory     | f        | t
(2 rows)
```
됐다. 원래 게획은 이런 방법으로 안되서 결국 manual에 나온 방법
```
ALTER USER tory CREATEDB;
```
으로 해야한다 였다. 그런데 결국 이 방법은 test도 안해봤다.
끝.








