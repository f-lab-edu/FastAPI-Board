from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from schemas.post import Post, ResponsePost, RequestPost

app = FastAPI()
post_data = {}


@app.get("/", status_code=status.HTTP_200_OK)
def read_root() -> dict[str, str]:
    """
    메인페이지
    루트 경로 접속 시, 세션을 설정한다.
    :return: 루트 경로 접속 시, 메시지를 반환합니다.
    """

    return {"msg": "F-LAB FastAPI"}


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
def read_post(post_id: UUID) -> ResponsePost:
    """
    게시글 조회
    :param post_id: 조회할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 반환합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    try:
        return post_data[post_id]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다.")


@app.post("/posts/", response_model=ResponsePost, status_code=status.HTTP_201_CREATED)
def create_post(post: RequestPost) -> ResponsePost:
    """
    게시글 생성
    :param post: 생성할 게시글의 내용 (author, title, content)
    :return: 생성 후 루트 경로로 리다이렉트합니다.
    """
    post = Post(**post.__dict__)
    post_data[post.id] = post

    return post
