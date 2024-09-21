from app.models import Note
from app.extensions import db
from sqlalchemy import or_


def get_notes(user_id, search_content=None):
    """Retrieve all notes for a user, with optional search by content."""
    if search_content:
        notes = (
            Note.query.filter_by(user_id=user_id)
            .filter(
                or_(
                    Note.title.ilike(f"%{search_content}%"),
                    Note.content.ilike(f"%{search_content}%"),
                )
            )
            .all()
        )
    else:
        notes = Note.query.filter_by(user_id=user_id).all()
    return notes


def get_note_by_id(note_id, user_id):
    """Retrieve a specific note by ID for a user."""
    return Note.query.filter_by(id=note_id, user_id=user_id).first()


def create_note(title, content, user_id):
    """Create a new note for a user."""
    new_note = Note(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()
    return new_note


def update_note(note_id, user_id, title, content):
    """Update an existing note for a user."""
    note = get_note_by_id(note_id, user_id)
    if not note:
        return None
    note.title = title if title else note.title
    note.content = content if content else note.content
    db.session.commit()
    return note


def set_note_remainder(note_id, user_id, email, remainder_time):
    """Set a remainder for a specific note."""
    note = get_note_by_id(note_id, user_id)
    if not note:
        return None
    note.email = email
    note.remainder_time = remainder_time
    db.session.commit()
    return note


def delete_note(note_id, user_id):
    """Delete a note for a user."""
    note = get_note_by_id(note_id, user_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return True
    return False
