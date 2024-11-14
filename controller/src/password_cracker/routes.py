from flask import render_template, request, redirect, url_for
from . import password_cracker_bp
from .models import Crack_john
from .forms import JohnForm
from src.exceptions import EndpointNotSet, RequestError
from src.errorhandler import handle_error
from sqlalchemy.exc import OperationalError
from requests import ConnectionError
import os
import requests
import json

cracks_john = []
endpoint = os.environ["PASSWORD_CRACKER_ENDPOINT"]
endpoint = os.environ["PASSWORD_CRACKER_ENDPOINT"] if os.environ["PASSWORD_CRACKER_ENDPOINT"] else 'http://127.0.0.1:3000'

def get_cracks_john() -> None:
    """
    This function retrieves all the john cracks from the database and puts them into the "cracks_john" list

    Arguments
    ---------
    None

    Returns
    -------
    None

    Exceptions
    ---------- 
    OperationalError -> Thrown if the database is not working
    """
    global cracks_john
    cracks_john = []    # Sets scans to an empty array, so the scans wont be added there twice


    for crack_john in Crack_john.query.all():
        cracks_john.append({
            'id': crack_john.id,
            'filename': crack_john.filename,
            'hash_format': crack_john.hash_format,
            'attack_type': crack_john.attack_type,
            'crack_json': crack_john.crack_json
        })


@password_cracker_bp.route("/password_cracker")
def password_cracker():
    """
    This is the default password cracker route. It contains a little navigation between the different utilities of the password cracker

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")  # Check if the scanner node is alive

        if endpoint_test.status_code == 200:
            return render_template('password_cracker.html'), 200
        
        else:
            raise ConnectionError

    except ConnectionError as e: 
        try:
            raise EndpointNotSet("Endpoint Not Set") 
        except Exception as e:
            r = handle_error(e)   
            return r, 400

    except Exception as e:
        r = handle_error(e)
        return r, 500

@password_cracker_bp.route("/password_cracker/john", methods=['GET', 'POST'])
def john():
    """
    This is the password cracker John route. It contains the John form and a list of all attempted password crackings

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    OperationalError -> Thrown if updating the 'cracks_john' array fails because of a database malfunction
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")  # Check if the password cracker node is alive

        if endpoint_test.status_code == 200:
            johnform = JohnForm()
            global cracks_john

            get_cracks_john()

            if request.method == 'POST' and johnform.validate():
                file = johnform.file.data
                format = johnform.format.data
                attack_type = johnform.attack_type.data
                dictionary = johnform.dictionary.data

                requests.post(url=f"{endpoint}/@crack_john?filename={file.filename}&format={format}&attack_type={attack_type}", 
                            files={"file": file, "dictionary": dictionary})

                return redirect(url_for('john'))

            return render_template('john.html', johnform=johnform, cracks_john=cracks_john), 200
        
        else:
            raise ConnectionError

    except ConnectionError as e:    
        try:
            raise EndpointNotSet(f"Endpoint Not Set")  
        except Exception as e:
            r = handle_error(e)   
            return r, 400
    
    except OperationalError as e:
        r = handle_error(e)
        return r, 500 

    except Exception as e:
        r = handle_error(e)
        return r, 500

@password_cracker_bp.route("/password_cracker/crack_john")
def crack_john():
    """
    This is the crack John route. It contains all information about a specific password cracking attempt

    Exception
    ---------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    OperationalError -> Thrown if updating the 'cracks_john' array fails because of a database malfunction

    RequestError -> Thrown if there is a problem with the request, e. g. invalid parameters
    """
    try:
        endopoint_test = requests.get(f"{endpoint}/@test")    # Check if the password cracker node is alive

        if endopoint_test.status_code == 200:
            global cracks_john 
            crack_john_id = int(request.args.get('crack_john_id'))
            crack_john_json = {}

            get_cracks_john()

            if crack_john_id == None: 
                raise RequestError("Invalid Crack ID")
            
            for crack_john in cracks_john:
                if crack_john['id'] == crack_john_id:
                    crack_john_json = json.loads(crack_john['crack_json'])

            if not crack_john_json:   
                raise RequestError("Invalid Crack ID")

            return render_template('john_crack.html', cracks_john=crack_john_json), 200
        
        else:
            raise ConnectionError

    except ConnectionError as e:    
        try:
            raise EndpointNotSet(f"Endpoint Not Set")  
        except Exception as e:
            r = handle_error(e)   
            return r, 400

    except RequestError as e:
        r = handle_error(e)
        return r, 400
    
    except OperationalError as e:
        r = handle_error(e)
        return r, 500

    except Exception as e:
        r = handle_error(e)
        return r, 500





