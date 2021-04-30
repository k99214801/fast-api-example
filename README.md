# TEST-FAST-API

fast-api 예제

## 준비
파이썬 언어와 MySQL 서버 필요<br>
실제 개발은 파이썬 3.9.4, MySQL Ver 8.0.23 for osx10.16 on x86_64 환경에서 개발
```
python 3.9.x
MySQL 8.x
Docker
```

app/settings/base.py에서 MySQL 접속 정보 변경
```
DATABASE = {
    "users": {
        "engine": os.environ.get(
            "DB_ENGINE",
            "mysql+pymysql://{username}:{password}@{host}:{port}/users?charset=utf8mb4",
        ),
        "echo": os.environ.get("DB_ECHO", "False") == "True",
        "pool_size": 10,
        "pool_recycle": 3600,
        "max_overflow": 5,
    },
}
```

### MySQL 데이터베이스 및 테이블 생성
create_tables.sql 파일을 이용하여 데이터베이스 및 테이블 생성<br>
```
DBName: users
TableNames:
 - users
 - sessions
```

## 설치

```
$ pip install -r requirements/base.txt
```

### 실행
```
$ uvicorn server:create_app --host 127.0.0.1 --port 80
```

### Docker
도커 파일로 이미지 생성 후 실행
```bash
docker build -t {image_name} .
```
빌드 성공 메시지
```
=> exporting to image                                                                                                                                                                                                                            0.6s
=> => exporting layers                                                                                                                                                                                                                           0.6s
=> => writing image sha256:a146215d5342d2f4e2d33461423441798c2c00f9b50aa1ceffefaaee23979a6f                                                                                                                                                      0.0s
=> => naming to docker.io/library/{image_name}
```
도커 컨테이너 실행<br>
서버 접속 포트 80
```
docker run -d --name {container_name} -p 80:80 {image_name}
```
서버 접속
```
$ curl -X GET localhost
{"message":"Hello!! Server is Running"}
```
도커에서 구동 시 DB 접속 에러 해결<br>
컨테이너 아이피 정보를 DB 권한 정보에 추가 
```
2021-04-29T14:47:44.297568300Z WARNING:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
2021-04-29T14:47:44.298140300Z INFO:     Started server process [1]
2021-04-29T14:47:44.298162900Z INFO:     Waiting for application startup.
2021-04-29T14:47:44.298503400Z INFO:     Application startup complete.
2021-04-29T14:47:44.298903900Z INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
2021-04-29T14:48:01.982966100Z INFO:     172.17.0.1:59656 - "POST /v1/users HTTP/1.1" 307 Temporary Redirect
2021-04-29T14:48:01.991977000Z ERROR:root:(pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on '127.0.0.1' ([Errno 111] Connection refused)")
2021-04-29T14:48:01.992115600Z (Background on this error at: http://sqlalche.me/e/14/e3q8)
2021-04-29T14:48:01.992263300Z INFO:     172.17.0.1:59656 - "POST /v1/users/ HTTP/1.1" HTTPStatus.INTERNAL_SERVER_ERROR Internal Server Error
2021-04-29T14:52:31.153666800Z INFO:     172.17.0.1:59662 - "POST /v1/users HTTP/1.1" 307 Temporary Redirect
2021-04-29T14:52:31.158923600Z INFO:     172.17.0.1:59662 - "POST /v1/users/ HTTP/1.1" HTTPStatus.INTERNAL_SERVER_ERROR Internal Server Error
2021-04-29T14:52:31.158970100Z ERROR:root:(pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on '127.0.0.1' ([Errno 111] Connection refused)")
2021-04-29T14:52:31.159004100Z (Background on this error at: http://sqlalche.me/e/14/e3q8)

mysql> grant all privileges on users.* to '{username}'@'172.17.0.1' identified by '{password}';
```

## 테스트
pytest를 이용하여 커버리지를 확인
```
$ pytest --cov-report term-missing --cov=app app/tests/
---------- coverage: platform darwin, python 3.9.4-final-0 -----------
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
app/__init__.py                      0      0   100%
app/core/__init__.py                 0      0   100%
app/core/rdb.py                     44      4    91%   26-28, 47
app/exceptions.py                   58      3    95%   59, 65-66
app/models/__init__.py               0      0   100%
app/models/sessions.py              33      0   100%
app/models/users.py                 64      0   100%
app/routers/__init__.py              0      0   100%
app/routers/home.py                  7      0   100%
app/routers/users.py                34      0   100%
app/serializers/__init__.py          0      0   100%
app/serializers/users.py            25      0   100%
app/services/__init__.py             0      0   100%
app/services/authentication.py      16      0   100%
app/services/session.py             41      7    83%   11, 31-32, 40-41, 56-57
app/services/users.py               58     14    76%   24-25, 36-39, 50-51, 59-62, 72-73
app/settings/__init__.py             0      0   100%
app/settings/base.py                 4      0   100%
app/tests/__init__.py                0      0   100%
app/tests/setup.py                  21      1    95%   28
app/tests/test_core_rdb.py          10      0   100%
app/tests/test_home.py              12      0   100%
app/tests/test_login_logout.py      29      0   100%
app/tests/test_register.py          34      0   100%
app/tests/test_retrieve.py          37      0   100%
--------------------------------------------------------------
TOTAL                              527     29    94%
```