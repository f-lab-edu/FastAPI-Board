# F-LAB FASTAPI STUDY

---
FastAPI를 이용한 REST API 간단한 게시판을 구축한 프로젝트입니다.
pyenv를 사용하여 파이썬을 설치하였고, poetry를 이용하여 가상환경을 구축하여 패키지를 관리하였습니다.

# Start

---

## 사용 환경

---
- python 3.10.0
- fastapi 0.111.0
- uvicorn 0.30.1

## 환경 설정 및 동작

---
```shell
poetry install
poetry run uvicorn main:app --reload
```

# API 기능

---
- 게시글 생성 (Create Post)
- 게시글 조회 (Get Post)
- 게시글 목록 조회 (List Posts)