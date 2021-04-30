# TEST-FAST-API

엔라이즈 테스트 회원 관리 API 서버 문서

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


## API Doc
API 목록
* 회원 가입<br>
* 로그인<br>
* 로그아웃<br>
* 사용자 조회<br>
* 회원 탈퇴

### API 응답 포맷

API 응답 상태 코드
```
200: Success
201: Created
400: Bad Request
404: Not Found
500: Internal Server Error
```
2xx를 제외한 나머지 상태인 경우에는 아래와 같은 JSON 포맷 데이터가 전달 됩니다
```
{
    "error_code": 101,
    "message": "동일 아이디가 존재합니다"
}
```

에러 코드 
```
100: 세션키가 없는 경우
101: 동일 아이디가 존재하는 경우
102: 회원 정보를 찾을 수 없는 경우
103: 유효하지 않는 세션 정보 
500: 알 수 없는 서버 에러
```

### 회원 가입
아이디, 패스워드 정보로 회원 가입
```
Method: POST
URL: {host}/v1/users
Header: 
 - Content-Type: application/json
Request Body: 
    {
        "id": string,   # 사용자 아이디
        "password": string # 사용자 비밀번호
    }
Response Body:
    { 
        "uid": number,  # 사용자 고유 키
        "created_at": string # 사용자 가입 날짜
    }

example:
$ curl --location --request POST 'http://127.0.0.1/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "test101",
    "password": 5623
}'
{"uid":56,"created_at":"2021-04-29 23:34:31"}
```

### 로그인
아이디, 패스워드로 로그인
```
Method: PUT
URL: {host}/v1/users/session
Header: 
 - Content-Type: application/json
Request Body: 
    {
        "id": string,   # 사용자 아이디
        "password": string # 사용자 비밀번호
    }
Response Body:
    { 
        "uid": number,  # 사용자 고유 키
        "session": string # 사용자 세션 키. 헤더 정보 x-session-key 값에 사용 
    }

example:
$ curl --location --request PUT 'http://127.0.0.1:8000/v1/users/session' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "test101",
    "password": "5623"
}'
{"uid":55,"session":"FvDvfbDGV9gLS0O6k2mpSA"}
```

### 로그아웃
로그인 세션 키 정보로 로그아웃
```
Method: DELETE
URL: {host}/v1/users/session
Header: 
 - Content-Type: application/json
 - x-session-key: {session_key} # 로그인 응답 값에 있는 session 정보
Request Body: 
    null
Response Body:
    null
    
example:
$ curl --location --request DELETE 'http://127.0.0.1:8000/v1/users/session' \
--header 'x-session-key: BLTVbvut2d_rhIPJuLZmfw'
```

### 회원탈퇴
로그인 세션 키 정보로 회원 탈퇴<br>
** 로그아웃된 세션 키는 회원 탈퇴 불
```
Method: DELETE
URL: {host}/v1/users/
Header: 
 - Content-Type: application/json
 - x-session-key: {session_key} # 로그인 응답 값에 있는 session 정보
Request Body: 
    null
Response Body:
    {
        "leave_dt": string # 탈퇴 날짜
    }
    
example:
$ curl --location --request DELETE 'http://127.0.0.1:8000/v1/users' \
--header 'x-session-key: 1qofsYACz6CDpM2o_wHmpg'
{"leave_dt":"2021-04-30 00:13:23"}
```

### 사용자 조회

```
Method: PUT
URL: {host}/v1/users/{uid}
Path Parameter:
 - uid: 사용자 고유 키
Request Body: 
    null
Response Body:
    { 
        "uid": number, # 사용자 고유 키
        "id": string, # 사용자 아이디
        "created_at": string, # 가입 날짜
        "leave_dt"(optional): string, # 탈퇴 날짜
        "sessions" : [ # 로그인 세션 목록 
            "session_key": string, # 세션 키
            "created_dt": string, # 세션 생성 날짜
            "logout_dt": string(nullable), # 로그 아웃 날짜 
        ] 
    }

example:
$ curl --location --request GET 'http://127.0.0.1/v1/users/57'
{
  "uid": 57,
  "id": "test103",
  "created_at": "2021-04-30 00:17:02",
  "sessions": [
    {
      "session_key": "wVBO0ACJJelETMynpQ09Ww",
      "created_dt": "2021-04-30 00:17:41",
      "logout_dt": null
    },
    {
      "session_key": "cJtU0uX1djtYY_I3Gn7rJQ",
      "created_dt": "2021-04-30 00:17:40",
      "logout_dt": null
    },
    {
      "session_key": "YSM2YpJTZvYl5kYaddsHsw",
      "created_dt": "2021-04-30 00:17:40",
      "logout_dt": null
    },
    {
      "session_key": "BFbmdEVsdqDPyAn_lTXUmQ",
      "created_dt": "2021-04-30 00:17:16",
      "logout_dt": null
    }
  ]
}
```