from src import create_app
from src.error.errorhandler import handle_error
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os

if __name__ == "__main__":
    try:
        app, db = create_app()
        # Checking if the database is working    
        with app.app_context():
            db.session.execute(text("SELECT 1"))

        # Starting the app

        app.run(host="0.0.0.0", port=os.environ["RUNNING_PORT"], debug=True)

    except OperationalError as e:
        with app.app_context():
            r = handle_error(e)

    except Exception as e:
        with app.app_context():
            r = handle_error(e)