# CHOCO API (Python, Fastapi)

### 프로그램 폴더 구조

```sh
Github
├─app
│  ├─common
│  ├─database
│  ├─errors
│  ├─services
│  ├─middlewares
│  ├─models
│  ├─routes
│  └─utils
│  main.py
└─tests
    conftest.py
    test_{}.py
```

### 폴더 역할
- common: 변수의 정의
- database: DB연결 및 스키마 정의
- errors: 에러 케이스 정의 및 에러 반환값 정의
- service: API 데이터 처리 모듈
- middlewares: 미들웨어 관리
- models: API response model, requests body 정의
- routes: 라우터 정의
- utils: 유틸 함수 정의
- tests: pytest 사용을 위한 폴더


### 기술 스택
- Python 3.11
- Fastapi
- Mysql
- Docker
