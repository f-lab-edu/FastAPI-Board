import secrets
from datetime import datetime
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request
from starlette.responses import Response

from schemas.post import Post, ResponsePost, RequestPost

app = FastAPI()
post_data = {}

SECRETS_KEY_LENGTH = 32


@app.get("/", status_code=status.HTTP_200_OK)
def read_root() -> dict[str, str]:
    """
    메인페이지
    루트 경로 접속 시, 토큰을 설정한다.
    :return: 루트 경로 접속 시, 메시지를 반환합니다.
    """

    response = Response()
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
    "/posts/{post_id}",
    response_model=ResponsePost,
    status_code=status.HTTP_200_OK
)
def read_post(request: Request, post_id: UUID) -> ResponsePost:
    """
    게시글 조회
    :param post_id: 조회할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 반환합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    try:
        post = post_data[post_id]

        # 게시글 작성자인지 확인
        if request.cookies.get("token") != post.token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="작성자만 접근 가능합니다.")

        return post
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다.")


@app.post("/posts/", response_model=ResponsePost, status_code=status.HTTP_201_CREATED)
def create_post(request: Request, post: RequestPost) -> ResponsePost:
    """
    게시글 생성
    :param post: 생성할 게시글의 내용 (author, title, content)
    :return: 생성 후 루트 경로로 리다이렉트합니다.
    """
    post = Post(
        token=request.cookies.get("token"),
        **post.__dict__
    )
    post_data[post.id] = post

    return post

@app.patch(
    "/posts/{post_id}",
    response_model=ResponsePost,
    status_code=status.HTTP_200_OK
)
def update_post(request: Request, post_id: UUID, update_data: RequestPost) -> ResponsePost:
    """
    게시글 수정
    :param post_id: 수정할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 수정합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    try:
        post = post_data[post_id]

        # 게시글 작성자인지 확인
        if request.cookies.get("token") != post.token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="작성자만 변경 가능합니다.")

        # 게시글 내용 수정
        for key, value in update_data:
            setattr(post, key, value)

        # 업데이트 시간 설정
        post.updated_at = datetime.utcnow()

        return post
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다.")
