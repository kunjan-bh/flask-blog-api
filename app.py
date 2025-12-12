from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from resources.auth import auth_bp
from resources.posts import posts_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    @app.route('/')
    def index():
        return {"msg": "Welcome to the Flask Blog API. Use /posts for listing."}
    



    with app.app_context():
        db.create_all()


    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)