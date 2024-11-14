# This file is the main entrypoint of this app. It contains all the routes #

# Imports #
from flask import request
from . import main_bp
from src.exceptions import ParameterException
from src.errorhandler import handle_error
from .tasks import add_scan


# Routes #
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

        options = request.args.get('options')   # Get the options of the scan
        range = request.args.get('range')   # Get the range of the scan
        scan_type = request.args.get('scan_type')   # Get the scan type

        add_scan.delay(options, range, scan_type)   # Call Celery to execute and add the scan

        return '', 201

    except ParameterException as e:
        handle_error(e)
        return '', 400

    except Exception as e:
        handle_error(e)
        return '', 400





