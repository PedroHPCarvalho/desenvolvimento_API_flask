from http import HTTPStatus
from flask import Blueprint
from flask import Blueprint, request
from src.app import Post, db
from sqlalchemy import inspect

app = Blueprint('post', __name__, url_prefix="/posts")


def __create_post():
    data = request.json
    post = Post(title=data["title"],body=data["body"],author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()


def __list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {     
            "id": post.id,
            "author_id": post.author_id,
            "created": post.created,
            "title": post.title,
            "body": post.body
        }
        for post in posts
    ]


@app.route('/', methods=['POST', 'GET'])
def list_or_create_post():
    if request.method == "POST":
        __create_post()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"posts": __list_posts()}


@app.route('/<int:post_id>')
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {     
            "id": post.id,
            "author_id": post.author_id,
            "created": post.created,
            "title": post.title,
            "body": post.body
    } 

@app.route('/<int:post_id>', methods=["PATCH"])
def update_user(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
        db.session.commit()

    return{     
            "id": post.id,
            "author_id": post.author_id,
            "created": post.created,
            "title": post.title,
            "body": post.body
    } 

@app.route('/<int:post_id>', methods=["DELETE"])
def delete_user(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
    