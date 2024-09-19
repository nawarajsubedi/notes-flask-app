from app.models import Note
from app.extensions import ma

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True  # Deserialize to model instances
    
    # If you want to customize certain fields, you can do it like this:
    created_at = ma.DateTime(format='%Y-%m-%dT%H:%M:%S')