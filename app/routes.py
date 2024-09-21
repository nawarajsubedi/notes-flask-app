from flask import Blueprint, request, jsonify, g

from app.utils import (
    create_response,
    generate_jwt_token,
    parse_datetime,
    token_required,
)
from app.schemas import NoteSchema, UserSchema
from app.services.notes_background_service import schedule_notes_email_remainder
from app.services.user_service import authenticate_user, register_user
from app.services import note_service


main_bp = Blueprint("main", __name__)
note_schema = NoteSchema(many=True)
user_schema = UserSchema(many=True)


@main_bp.route("/notes", methods=["GET"])
@token_required
def get_all_notes():
    user = g.user
    try:
        search_content = request.args.get("search_content")
        notes = note_service.get_notes(user_id=user.id, search_content=search_content)
        notes_data = note_schema.dump(notes)
        return create_response("Notes retrieved successfully", 200, data=notes_data)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving notes.", 500, error=str(e)
        )


@main_bp.route("/notes/<int:note_id>", methods=["GET"])
@token_required
def get_note(note_id):
    user = g.user
    try:
        note = note_service.get_note_by_id(note_id=note_id, user_id=user.id)
        if note:
            note_data = NoteSchema().dump(note)
            return create_response("Note retrieved successfully", 200, data=note_data)
        return create_response("Note not found", 404)
    except Exception as e:
        return create_response(
            "An error occurred while retrieving the note.", 500, error=str(e)
        )


@main_bp.route("/notes", methods=["POST"])
@token_required
def save_notes():
    user = g.user
    try:
        json_data = request.get_json()
        new_note = note_service.create_note(
            title=json_data.get("title", ""),
            content=json_data.get("content", ""),
            user_id=user.id,
        )
        note_data = NoteSchema().dump(new_note)
        return create_response("Note created successfully", 201, data=note_data)
    except Exception as e:
        return create_response(
            "An error occurred while creating the note.", 500, error=str(e)
        )


@main_bp.route("/notes/<int:note_id>", methods=["PUT"])
@token_required
def update_note(note_id):
    user = g.user
    json_data = request.get_json()
    try:
        updated_note = note_service.update_note(
            note_id=note_id,
            user_id=user.id,
            title=json_data.get("title"),
            content=json_data.get("content"),
        )
        updated_note_data = NoteSchema().dump(updated_note)
        return create_response("Note updated successfully", 200, data=updated_note_data)
    except Exception as e:
        return create_response(
            "An error occurred while updating the note.", 500, error=str(e)
        )


@main_bp.route("/notes/<int:note_id>/set-remainder", methods=["PUT"])
@token_required
def set_notes_remainder(note_id):
    user = g.user
    json_data = request.get_json()
    try:
        updated_note = note_service.set_note_remainder(
            note_id=note_id,
            user_id=user.id,
            email=json_data["email"],
            remainder_time=parse_datetime(json_data["remainder_time"]),
        )

        note_schema = NoteSchema()
        updated_note_data = note_schema.dump(updated_note)
        schedule_notes_email_remainder.apply_async(
            kwargs={
                "email": json_data["email"],
                "title": updated_note.title,
                "content": updated_note.content,
            },
            eta=updated_note.remainder_time,
        )

        return create_response(
            "Note remainder updated successfully", 200, data={"note": updated_note_data}
        )
    except Exception as e:
        return create_response(
            "An error occurred while updating the note remainder.", 500, error=str(e)
        )


@main_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@token_required
def delete_note(note_id: int):
    user = g.user
    try:
        success = note_service.delete_note(note_id=note_id, user_id=user.id)
        if success:
            return create_response("Note deleted successfully", 200)
        else:
            return create_response("Note not found or not authorized to delete", 404)
    except Exception as e:
        return create_response(
            "An error occurred while deleting the note.", 500, error=str(e)
        )


@main_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return create_response("Missing data", 400)

    response, status_code = register_user(username, email, password)
    return create_response(response["message"], status_code)


@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return create_response("Missing data", 400)

    user, error = authenticate_user(username, password)
    if error:
        return create_response(error["message"], 401)

    token = generate_jwt_token(user.id)
    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return create_response(
        "Login successful", 200, data={"user": user_data, "token": token}
    )
