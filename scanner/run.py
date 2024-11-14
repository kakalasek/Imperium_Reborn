from src import create_app
from src.errorhandler import handle_error
from sqlalchemy.exc import OperationalError
import os

if __name__ == '__main__':
    try:
        app, db = create_app()

        with app.app_context():
            db.create_all() # Creates the tables

        app.run(host="0.0.0.0", port=os.getenv("RUNNING_PORT"), debug=True) 

    except OperationalError as e:
        handle_error(e)

    except Exception as e:
        handle_error(e)