import secrets
from datetime import datetime
from functools import wraps
from typing import Callable
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request
from starlette.responses import Response

from schemas.post import CreatePost, Post, ResponsePost, UpdatePost

app = FastAPI()
post_data = {}

SECRETS_KEY_LENGTH = 32


def verify_author(request: Request, post_id: UUID):
    """
    게시글 작성자 확인
    :param request: Request 객체
    :param post_id: 게시글 ID
    :return: None
    """
    post = post_data.get(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다."
        )

    if request.cookies.get("token") != post.token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="작성자만 접근 가능합니다."
        )


def author_verification(func: Callable):
    """
    게시글 작성자 확인 데코레이터
    :param func: 데코레이터를 적용할 함수
    :return: 데코레이터 함수
    """

    @wraps(func)
    def wrapper(request: Request, post_id: UUID, *args, **kwargs):
        verify_author(request, post_id)
        return func(request, post_id, *args, **kwargs)

    return wrapper


@app.get("/", status_code=status.HTTP_200_OK)
def read_root() -> Response:
    """
    메인페이지
    루트 경로 접속 시, 토큰을 설정한다.
    :return: 루트 경로 접속 시, 메시지를 반환합니다.
    """

    response = Response("F-LAB FastAPI Study 게시판", media_type="text/plain")
    response.set_cookie(key="token", value=secrets.token_hex(SECRETS_KEY_LENGTH))

    return response


@app.get("/posts/", response_model=list[ResponsePost], status_code=status.HTTP_200_OK)
def read_posts() -> list[ResponsePost]:
    """
    게시글 목록 조회
    :return: 게시글 목록과 각 게시글의 URL을 포함한 리스트를 반환합니다.
    """
    return post_data.values()


@app.get(
    "/posts/{post_id}", response_model=ResponsePost, status_code=status.HTTP_200_OK
)
def read_post(request: Request, post_id: UUID) -> ResponsePost:
    """
    게시글 조회
    :param post_id: 조회할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 반환합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    return post_data[post_id]


@app.post("/posts/", response_model=ResponsePost, status_code=status.HTTP_201_CREATED)
def create_post(request: Request, post: CreatePost) -> ResponsePost:
    """
    게시글 생성
    :param post: 생성할 게시글의 내용 (author, title, content)
    :return: 생성 후 루트 경로로 리다이렉트합니다.
    """
    post = Post(token=request.cookies.get("token"), **post.__dict__)
    post_data[post.id] = post

    return post


@app.patch(
    "/posts/{post_id}", response_model=ResponsePost, status_code=status.HTTP_200_OK
)
@author_verification
def update_post(
    request: Request, post_id: UUID, update_data: UpdatePost
) -> ResponsePost:
    """
    게시글 수정
    :param post_id: 수정할 게시글의 ID
    :param update_data: 수정할 게시글의 내용 (author, title, content)
    :return: 특정 ID를 가진 게시글의 내용을 수정합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """

    # 수정을 위해 게시글 데이터 가져오기
    post = post_data[post_id]

    # 게시글 내용 수정
    for key, value in update_data:
        if value:
            setattr(post, key, value)

    # 업데이트 시간 재설정
    post.updated_at = datetime.utcnow()

    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
@author_verification
def delete_post(request: Request, post_id: UUID) -> dict[str, str]:
    """
    게시글 삭제
    :param post_id: 삭제할 게시글의 ID
    :return: 특정 ID를 가진 게시글을 삭제합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    del post_data[post_id]

    return {"message": "게시글이 삭제되었습니다."}
