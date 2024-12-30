"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

from src.models import db

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    scan_json = db.Column(db.Text, nullable=False)