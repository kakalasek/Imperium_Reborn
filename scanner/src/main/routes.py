"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

from flask import request
from . import main_bp
from src.exceptions import ParameterException
from src.errorhandler import handle_error
from .tasks import add_scan

@main_bp.route("/@test")    
def test():
    """
    This is the test route for this app. It checks if this app is alive and working 
    """
    return '', 200

@main_bp.route("/@scan", methods=["POST"])  
def scan():
    """
    This route checks the parameters and calls the scan task to perform the scan

    Exceptions
    ----------
    ParemeterException -> Thrown if any of the parameters is either missing or invalid
    """
    try:
        if 'options' not in request.args:
            raise ParameterException("Options parameter is missing from the request")
        
        if 'range' not in request.args:
            raise ParameterException("Range parameter is missing from the request")
        
        if 'scan_type' not in request.args:
            raise ParameterException("Scan type parameter is missing from the request")

        options = request.args.get('options') 
        range = request.args.get('range')  
        scan_type = request.args.get('scan_type')   

        add_scan.delay(options, range, scan_type) 

        return '', 201

    except ParameterException as e:
        handle_error(e)
        return '', 400

    except Exception as e:
        handle_error(e)
        return '', 400





