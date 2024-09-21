This is a simple Note Taker application built with Flask, using PostgreSQL for data storage, Celery for background tasks (like sending email reminders), and SendGrid to send emails.

## Prerequisites

- Python 3.9
- PostgreSQL
- Redis (for Celery task queue)
- SendGrid account (for email notifications)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nawarajsubedi/notes-flask-app.git
   cd notes-flask-app
   ```

2. Create a virtual environment and activate it:
    ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use venv\Scripts\activate\
    ```

3.Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.Set up environment variables: Create a .env file with the following:
  ```bash
      DATABASE_URL=postgresql://<user>:<password>@localhost/<database_name>
      SENDGRID_API_KEY=<your_sendgrid_api_key>
      REDIS_URL=redis://localhost:6379/0
  ```
4.Set up environment variables: Create a .env file with the following:
  ```bash
  DATABASE_URL=postgresql://<user>:<password>@localhost/<database_name>
  SENDGRID_API_KEY=<your_sendgrid_api_key>
  REDIS_URL=redis://localhost:6379/0
```
5.Running the Application
  ```bash
- Initialize the database (if necessary):
flask --app main init-db
- Start the Flask development server:
flask --app main --debug run
- Run Celery worker for background tasks:
celery -A main.celery worker --loglevel=info
```
## Features
- Note Creation: Users can create, update, delete, and manage notes.
- Auto-Save: Notes auto-save every few seconds while the user is typing.
- Reminder Setup: Users can set a reminder for notes, and receive email notifications.

## Task Scheduling with Celery
This application uses Celery to schedule email reminders asynchronously, ensuring the app remains responsive while background tasks are processed.

