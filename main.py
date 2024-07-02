import secrets
from datetime import datetime
from uuid import UUID

from fastapi import Cookie, Depends, FastAPI, HTTPException, status
from starlette.responses import Response

from schemas.base import ResponseModel
from schemas.post import CreatePost, Post, ResponsePost, UpdatePost

app = FastAPI()
post_data = {}

SECRETS_KEY_LENGTH = 32


def get_token(token: str = Cookie(None)) -> str:
    """
    토큰 가져오기
    :param token: 사용자의 토큰
    :return: 사용자의 토큰을 반환합니다.
    """
    return token


def verify_post_id(post_id: UUID) -> Post:
    """
    게시글 가져오기
    :param post_id: 게시글 ID
    :return: 게시글 객체
    """
    post = post_data.get(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다."
        )

    return post


def verify_author(post_id: UUID, token: str | None = Cookie(None)) -> Post:
    """
    게시글 작성자 확인
    :param token: 사용자의 토큰
    :param post_id: 게시글 ID
    :return: 게시글 객체
    """
    post = verify_post_id(post_id)

    if token != post.token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="작성자만 접근 가능합니다."
        )

    return post


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


@app.get(
    "/posts/",
    response_model=ResponseModel[ResponsePost],
    status_code=status.HTTP_200_OK,
)
def read_posts() -> ResponseModel[ResponsePost]:
    """
    게시글 목록 조회
    :return: 게시글 목록과 각 게시글의 URL을 포함한 리스트를 반환합니다.
    """
    return ResponseModel(count=len(post_data), items=post_data.values())


@app.get(
    "/posts/{post_id}", response_model=ResponsePost, status_code=status.HTTP_200_OK
)
def read_post(post=Depends(verify_post_id)) -> ResponsePost:
    """
    게시글 조회
    :param post_id: 조회할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 반환합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    return post


@app.post("/posts/", response_model=ResponsePost, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, token=Depends(get_token)) -> ResponsePost:
    """
    게시글 생성
    :param post: 생성할 게시글의 내용 (author, title, content)
    :return: 생성 후 루트 경로로 리다이렉트합니다.
    """
    post = Post(token=token, **post.__dict__)
    post_data[post.id] = post

    return post


@app.patch(
    "/posts/{post_id}", response_model=ResponsePost, status_code=status.HTTP_200_OK
)
def update_post(
    post_id: UUID, update_data: UpdatePost, depends=Depends(verify_author)
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
def delete_post(post_id: UUID, depends=Depends(verify_author)) -> dict[str, str]:
    """
    게시글 삭제
    :param post_id: 삭제할 게시글의 ID
    :return: 특정 ID를 가진 게시글을 삭제합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    del post_data[post_id]

    return {"message": "게시글이 삭제되었습니다."}
