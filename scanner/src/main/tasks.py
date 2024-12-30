"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

from celery import shared_task
import subprocess
import xmltodict
import json
from .models import Scan
from src.models import db
from src.errorhandler import handle_error

@shared_task()
def add_scan(options: str, range: str, scan_type: str) -> None:
    """
    This task initiates the scan and adds it into the database

    Arguments
    ---------
    options -> Those are the special options for the scan
    range -> These are the adresses or domains to be scanned
    scan_type -> Type of the scan as string

    Exceptions
    ----------
    OperationalError -> Thrown if there is a database malfunction
    """    
    try:
        xml_content = subprocess.getoutput(f"nmap -oX - {options} {range}")
        data_dict = xmltodict.parse(xml_content)

        json_output = data_dict['nmaprun']
        json_output = json.dumps(json_output) 
                
        new_scan = Scan(name=scan_type, target=range, scan_json=json_output)    
        db.session.add(new_scan)
        db.session.commit()
    
    except Exception as e:
        handle_error(e)
