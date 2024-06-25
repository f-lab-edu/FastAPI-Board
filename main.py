from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
post_data = []


class Post(BaseModel):
    id: int = Field(default_factory=lambda: len(post_data))
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now)


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    메인페이지
    루트 경로 접속 시, 세션을 설정한다.
    :return: 루트 경로 접속 시, 메시지를 반환합니다.
    """

    return {"msg": "F-LAB FastAPI"}


@app.get("/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def read_posts() -> list[dict]:
    """
    게시글 목록 조회
    :return: 게시글 목록과 각 게시글의 URL을 포함한 리스트를 반환합니다.
    """
    return [
        {
            "post_id": post.id,
            "url": f"/posts/{post.id}"
        }
        for post in post_data
    ]


@app.get(
    "/posts/{post_id}",
    response_model=Post,
    status_code=status.HTTP_200_OK
)
def read_post(post_id: int):
    """
    게시글 조회
    :param post_id: 조회할 게시글의 ID
    :return: 특정 ID를 가진 게시글의 내용을 반환합니다. 존재하지 않는 게시글 ID인 경우 404 에러를 발생시킵니다.
    """
    try:
        return post_data[post_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")


@app.post("/posts/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    게시글 생성
    :param post: 생성할 게시글의 내용 (author, title, content)
    :return: 생성 후 루트 경로로 리다이렉트합니다.
    """
    post_data.append(post)
    return post
