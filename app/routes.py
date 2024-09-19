from flask import Blueprint, request, jsonify, g
from app.models import Note, User
from app.extensions import db
from app.schemas import NoteSchema
from app.utils import generate_jwt_token, parse_datetime, token_required
from app.services import note_service


main_bp = Blueprint("main", __name__)
note_schema = NoteSchema(many=True)


@main_bp.route("/notes")
@token_required
def get_all_notes():
    user = g.user
    try:
        notes = note_service.get_notes(user_id=user.id)
        notes_data = note_schema.dump(notes)

        return (
            jsonify({"data": notes_data}),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while creating the note.",
                    "error": str(e),
                }
            ),
            500,
        )


@main_bp.route("/notes", methods=["POST"])
@token_required
def save_notes():
    user = g.user
    try:
        json_data = request.get_json()
        new_note = Note(
            title=json_data.get("title"),
            content=json_data.get("content"),
            user_id=user.id,
        )
        note_service.save_notes(new_note)
        note_schema = NoteSchema()
        return (
            jsonify(
                {
                    "message": "Note created successfully!",
                    "data": note_schema.dump(new_note),
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while creating the note.",
                    "error": str(e),
                }
            ),
            500,
        )


@main_bp.route("/notes/<int:note_id>", methods=["PUT"])
@token_required
def update_note(note_id):
    """
    Update an existing note by its ID.
    """
    user = g.user

    json_data = request.get_json()

    if not json_data or not json_data.get("title") or not json_data.get("content"):
        return (
            jsonify({"message": "Invalid input. Title and content are required."}),
            400,
        )

    note = note_service.get_note_by_id(note_id, user.id)

    if not note:
        return (
            jsonify(
                {"message": "Note not found or you don't have permission to edit it."}
            ),
            404,
        )

    updated_note = note_service.update_notes(
        note, json_data["title"], json_data["content"]
    )

    # Serialize the updated note
    note_schema = NoteSchema()
    updated_note_data = note_schema.dump(updated_note)

    # Return the response
    return (
        jsonify({"message": "Note updated successfully!", "data": updated_note_data}),
        200,
    )


@main_bp.route("/notes/<int:note_id>/set-remainder", methods=["POST"])
@token_required
def set_notes_remainder(note_id):
    """
    Update an existing note remainder by its ID.
    """
    user = g.user

    json_data = request.get_json()

    # if not json_data or not json_data.get("title") or not json_data.get("content"):
    #     return (
    #         jsonify({"message": "Invalid input. Title and content are required."}),
    #         400,
    #     )

    note = note_service.get_note_by_id(note_id, user.id)

    if not note:
        return (
            jsonify(
                {"message": "Note not found or you don't have permission to edit it."}
            ),
            404,
        )

    updated_note = note_service.update_schedule_email(
        note, json_data["email"], parse_datetime(json_data["remainder_time"])
    )

    note_schema = NoteSchema()
    updated_note_data = note_schema.dump(updated_note)

    return (
        jsonify({"message": "Note remainder updated successfully!", "data": updated_note_data}),
        200,
    )


@main_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@token_required
def delete_note(note_id: int):
    """
    Delete a note by its ID.
    :param note_id: ID of the note to delete
    :return: JSON response with success or failure message
    """
    user = g.user  # Get the user object from the token

    note = note_service.get_note_by_id(note_id, user.id)

    if not note:
        return (
            jsonify(
                {"message": "Note not found or you don't have permission to edit it."}
            ),
            404,
        )

    success = note_service.delete_note_by_id(note_id=note_id)

    if success:
        return jsonify({"message": "Note deleted successfully!"}), 200
    else:
        return jsonify({"error": "Note not found or not authorized to delete"}), 404

    update_schedule_email


@main_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing data"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    print(f"password: {len(new_user.password_hash)}: {new_user.password_hash}")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    print(f"username: {username}, password:{password}")
    if not username or not password:
        return jsonify({"message": "Missing data"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    token = generate_jwt_token(user.id)

    # Normally, you would generate a JWT token or session here
    return jsonify({"message": "Login successful", "token": token}), 200
