from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import User


def register_user(username, email, password):
    try:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "User already exists"}, 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created"}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500


def authenticate_user(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return {"message": "Invalid username or password"}, 401

        return user, None
    except SQLAlchemyError as e:
        return None, {"message": str(e)}, 500
