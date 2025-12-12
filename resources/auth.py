from flask import Blueprint, request, jsonify
from extensions import db, jwt
from models import User, TokenBlocklist
from flask_jwt_extended import create_access_token, jwt_required, get_jwt


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"msg": "Missing fields"}), 400
    if User.query.filter((User.username==username)|(User.email==email)).first():
        return jsonify({"msg": "User with that username or email already exists"}), 409
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created", "user": user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti'] 
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({"msg": "Successfully logged out"}), 200

# Token-in-blocklist check
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    jti = jwt_payload.get('jti')
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

