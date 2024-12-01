"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField 
from wtforms.validators import DataRequired


class ScanForm(FlaskForm): 
    ip = StringField('IP Adress or Range',
                       validators=[DataRequired()])
    scan_type = SelectField("Scan Type", choices=[('-sS', 'Syn Scan'), 
                                                  ('-sV', 'Version Scan'), 
                                                  ('-O', 'System Scan'), 
                                                  ('-sF', 'Fin Scan'), 
                                                  ('-sU', 'UDP Scan'), 
                                                  ('-sT', 'Connect Scan')])
    no_ping = BooleanField("No Ping")
    randomize_hosts = BooleanField("Randomize Hosts")
    fragment_packets = BooleanField("Fragment Packets")
    submit = SubmitField('Scan')