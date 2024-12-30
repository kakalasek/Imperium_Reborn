"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

from src import create_app
from src.errorhandler import handle_error
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os

if __name__ == "__main__":
    try:
        app, db = create_app()

        app.run(host="0.0.0.0", port=os.getenv("RUNNING_PORT"), debug=True)

    except OperationalError as e:
        with app.app_context():
            r = handle_error(e)

    except Exception as e:
        with app.app_context():
            r = handle_error(e)