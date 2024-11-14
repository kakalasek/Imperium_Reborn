from flask import render_template, request, redirect, url_for
from . import scanner_bp
from .models import Scan
from .forms import ScanForm
from src.exceptions import EndpointNotSet, RequestError
from sqlalchemy.exc import OperationalError
from src.errorhandler import handle_error
from requests.exceptions import ConnectionError
import requests
import os
import json

scans = []
endpoint = os.environ["SCANNER_ENDPOINT"] if os.environ["SCANNER_ENDPOINT"] else 'http://127.0.0.1:3000'

def get_scans() -> None:   
    """
    This function retrieves all the scans from the database and puts them into the "scans" list

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
    global scans
    scans = []  # Sets scans to an empty array, so the scans wont be added there twice

    for scan in Scan.query.all():   
            scans.append({
                'id': scan.id,
                'name': scan.name,
                'target': scan.target,
                'scan_json': scan.scan_json
            })

@scanner_bp.route('/scanner', methods=['GET', 'POST'])
def scanner():
    """
    This is the default scanner route. It contains the scan form and a list of all initiated scans

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    OperationalError -> Thrown if updating the 'scans' array fails because of a database malfunction
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")    # Check if the scanner node is alive

        # Checking the returned status code, just to be sure
        if endpoint_test.status_code == 200:
            scanform = ScanForm()

            get_scans() 

            if request.method == 'POST' and scanform.validate():    
                options = scanform.scan_type.data   
                scan_name = 'Scan'
                scan_range = scanform.ip.data 

                match options: 
                    case '-sS':
                        scan_name = 'SYN Scan'
                    case '-sV':
                        scan_name = 'Version Scan'
                    case '-O':
                        scan_name = 'System Scan'
                    case '-sF':
                        scan_name = 'Fin Scan'
                    case '-sU':
                        scan_name = 'UDP Scan'
                    case '-sT':
                        scan_name = 'Connect Scan'

                if scanform.no_ping.data:   
                    options += " -Pn"
                if scanform.randomize_hosts.data:
                    options += " --randomize-hosts"
                if scanform.fragment_packets.data:
                    options += " -f"

                requests.post(f"{endpoint}/@scan?range={scan_range}&options={options}&scan_type={scan_name}")
                return redirect(url_for("scanner_bp.scanner"))

            return render_template('scanner.html', scanform=scanform, scans=scans), 200
        else:
            raise ConnectionError
        
    except ConnectionError as e:    
        try:
            raise EndpointNotSet("Endpoint Not Set")  # Just to have that "Endpoint Not Set" in the message
        except Exception as e:
            r = handle_error(e)   
            return r, 400

    except OperationalError as e:
        r = handle_error(e)
        return r, 500

    except Exception as e:
        r = handle_error(e)
        return r, 500
    
@scanner_bp.route("/scanner/scan") 
def scan():
    """
    This is the scan route. It contains the list of all found hosts in a particular scan

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    OperationalError -> Thrown if updating the 'scans' array fails because of a database malfunction

    RequestError -> Thrown if there is a problem with the request, e. g. invalid parameters
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")    # Check if the scanner node is alive

        if endpoint_test.status_code == 200:
            get_scans() 

            global scans
            scan_id = request.args.get('scan_id')
            scan_json = {}  # JSON for this particular scan will be stored here

            if scan_id == None: 
                raise RequestError("Invalid Scan ID")

            for scan in scans: # Check for each entry in the scans table. If the scan is found, load it into 'scan_json' and break
                if scan["id"] == int(scan_id):
                    scan_json = json.loads(scan["scan_json"])
                    break
            
            if not scan_json:   
                raise RequestError("Invalid Scan ID")
            
            return render_template('scan.html', scan_json=scan_json, scan_id=scan_id), 200
        else:
            raise ConnectionError

    except ConnectionError as e:    
        try:
            raise EndpointNotSet("Endpoint Not Set")   # Just to have that "Endpoint Not Set" in the message
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

@scanner_bp.route("/scanner/host")
def host():
    """
    This is the host route. It contains all the information about a particular host in a particular scan

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    OperationalError -> Thrown if updating the 'scans' array fails because of a database malfunction

    RequestError -> Thrown if there is a problem with the request, e. g. invalid parameters
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")    # Check if the scanner node is alive

        if endpoint_test.status_code == 200:

            global scans
            without_mac = True  # Is here because the json looks differently depending on if the scan was able to determine the MAC address or not
            scan_id = int(request.args.get('scan_id'))
            host_ip = request.args.get('host_ip')
            host_json = {}

            get_scans()

            if scan_id == None: 
                raise RequestError("Invalid Scan ID")
            
            if host_ip == None: 
                raise RequestError("Invalid Host IP")

            for scan in scans:
                if scan["id"] == scan_id:
                    scan_json = json.loads(scan["scan_json"])

                    if isinstance(scan_json['host'], dict): # If scan_json['host'] is a dictionary a single host was scanned, so there is no need for further ip control

                        if "@addr" in scan_json['host']['address']: 
                            host_json = scan_json['host']
                        else:
                            host_json = scan_json['host']
                            without_mac = False

                    else:   # Multiple hosts were scanned, so the right one must be found
                        for host in scan_json['host']:

                            if "@addr" in host['address']: 
                                if host['address']['@addr'] == host_ip:
                                    host_json = host
                                    break

                            elif host['address'][0]['@addr'] == host_ip:
                                host_json = host
                                without_mac = False
                                break
                    break
                

            if not host_json:   
                raise RequestError("Invalid Scan ID or Host IP")
            
            print("hi")

            return render_template('host.html', data=host_json, without_mac=without_mac, scan_id =scan_id, host_ip=host_ip), 200
        else:
            raise ConnectionError

    except ConnectionError as e:  
        try:
            raise EndpointNotSet("Endpoint Not Set") 
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

@scanner_bp.route("/scanner/scan/show_json") 
def show_json():
    """
    This the scanner show JSON route. It simply renders the whole json for a particular scan or host

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    RequestError -> Thrown if there is a problem with the request, e. g. invalid parameters
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")    # Check if the scanner node is alive

        if endpoint_test.status_code == 200:
            global scans
            scan_id = int(request.args.get('scan_id'))
            host_json = {}
            scan_json = {}

            if scan_id == None: 
                raise RequestError("Invalid Scan ID")

            if request.args.get('host_ip'): # For JSON of a host
                host_ip = request.args.get('host_ip')

                for scan in scans: 
                    if scan["id"] == scan_id: 
                        scan_json = json.loads(scan["scan_json"])

                        if isinstance(scan_json['host'], dict): # If scan_json['host'] is a dictionary a single host was scanned, so there is no need for further ip control
                            if "@addr" in scan_json['host']['address']: 
                                host_json = scan_json['host']
                                return host_json, 200

                            else:
                                host_json = scan_json['host']
                                return host_json, 200

                        else:   # Multiple hosts were scanned, so the right one must be found
                            for host in scan_json['host']: 
                                if "@addr" in host['address']:  
                                    if host['address']['@addr'] == host_ip:
                                        host_json = host
                                        return host_json, 200

                                elif host['address'][0]['@addr'] == host_ip:
                                    host_json = host
                                    return host_json, 200

                        break

                if not host_json:  
                    raise RequestError("Invalid Scan ID or Host IP")
                    
            else:   # For JSON of a scan
                for scan in scans: 
                    if scan["id"] == scan_id:
                        scan_json = json.loads(scan["scan_json"])
                        return scan_json, 200
                    
                if not scan_json:  
                    raise RequestError("Invalid Scan ID")
        else:
            raise ConnectionError 
    
    except ConnectionError as e: 
        try:
            raise EndpointNotSet("Endpoint Not Set")   
        except Exception as e:
            r = handle_error(e)   
            return r, 400

    except RequestError as e:
        r = handle_error(e)
        return r, 400

    except Exception as e:
        r = handle_error(e)
        return r, 500
