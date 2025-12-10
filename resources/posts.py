from flask import Blueprint, request, jsonify, abort
from extensions import db
from models import Post, User
from flask_jwt_extended import jwt_required, get_jwt_identity


posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('', methods=['GET'])
def list_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    q = Post.query.order_by(Post.created_at.desc())
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    posts = [p.to_dict() for p in pagination.items]
    return jsonify({
        'posts': posts,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'total_pages': pagination.pages
    })

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({"msg": "Missing title or content"}), 400
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    post = Post(title=title, content=content, author=user)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = int(get_jwt_identity())
    if post.author_id != user_id:
        return jsonify({"msg": "You are not the author"}), 403
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    if title:
        post.title = title
    if content:
        post.content = content
    db.session.commit()
    return jsonify(post.to_dict())

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = int(get_jwt_identity())
    if post.author_id != user_id:
        return jsonify({"msg": "You are not the author"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted"}), 200