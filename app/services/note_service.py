from datetime import datetime
from app.extensions import db
from app.models import Note

def get_note_by_id(note_id, user_id):
    """
    Fetch a note by its ID and user ID.
    """
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    return note

def save_notes(note: Note):
    db.session.add(note)
    db.session.commit()
    return note

def get_notes(user_id: int):
    notes = Note.query.filter_by(user_id=user_id).all()
    return notes


def update_notes(note: Note, title, content):
    """
    Update the note with new title and content.
    """
    note.title = title
    note.content = content

    # Commit the changes to the database
    db.session.commit()

    return note

def delete_note_by_id(note_id: int) -> bool:
    """
    Delete a note by its ID.
    :param note_id: ID of the note to delete
    :return: True if deletion was successful, False otherwise
    """
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return True
    return False

def update_schedule_email(note: Note, email: str, remainder_time: datetime):
    """
    Update the note with email and remainder time.
    """
    note.email = email
    note.reminder_time = remainder_time

    db.session.commit()

    return note