import os

from flask_mail import Mail
from app import create_app, celery_init_app


app = create_app()
celery = celery_init_app(app)
mail = Mail(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
