"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

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
endpoint = os.getenv("SCANNER_ENDPOINT") if os.getenv("SCANNER_ENDPOINT") else 'http://127.0.0.1:3000'

def get_scans() -> None:   
    """
    This function retrieves all the scans from the database and puts them into the "scans" list

    Exceptions
    ---------- 
    OperationalError -> Thrown if the database is not working
    """
    global scans
    scans = []

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
        endpoint_test = requests.get(f"{endpoint}/@test")

        if endpoint_test.status_code == 200:

            get_scans() 

            scanform = ScanForm()
            global scans

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
            raise EndpointNotSet("Endpoint Not Set")
        except Exception as e:
            r = handle_error(e)   
            return r, 400

    except OperationalError as e:
        r = handle_error(e)
        return r, 500

    except Exception as e:
        r = handle_error(e)
        return r, 500
    
@scanner_bp.route("/scanner/scan", methods=['GET']) 
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
        endpoint_test = requests.get(f"{endpoint}/@test")

        if endpoint_test.status_code == 200:
            get_scans() 

            global scans
            scan_id = request.args.get('scan_id')
            scan_json = {}

            if scan_id == None: 
                raise RequestError("Scan ID not provided")

            for scan in scans:
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

@scanner_bp.route("/scanner/host", methods=['GET'])
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
        endpoint_test = requests.get(f"{endpoint}/@test")

        if endpoint_test.status_code == 200:
            get_scans()

            global scans
            mac_address_found = True
            scan_id = int(request.args.get('scan_id'))
            host_ip = request.args.get('host_ip')
            host_json = {}

            if scan_id == None: 
                raise RequestError("Scan ID not provided")
            
            if host_ip == None: 
                raise RequestError("Host ID not provided")

            for scan in scans:
                if scan["id"] == scan_id:
                    scan_json = json.loads(scan["scan_json"])

                    single_host_scanned = isinstance(scan_json['host'], dict)

                    if single_host_scanned:

                        host_json = scan_json['host']
                        mac_address_found = not "@addr" in host_json['address']

                    else:
                        hosts = scan_json['host']

                        for host in hosts:

                            mac_address_found = isinstance(host['address'], list)

                            if mac_address_found:
                                if host['address'][0]['@addr'] == host_ip:
                                    host_json = host
                                    break
                            else:
                                if host['address']['@addr'] == host_ip:
                                    host_json = host
                                    break
                    break
                

            if not host_json:   
                raise RequestError("Invalid Scan ID or Host IP")
            
            return render_template('host.html', data=host_json, mac_address_found=mac_address_found, scan_id=scan_id, host_ip=host_ip), 200
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

@scanner_bp.route("/scanner/scan/show_json", methods=['GET']) 
def show_json():
    """
    This is the scanner show JSON route. It simply renders the whole json for a particular scan or host

    Exceptions
    ----------
    ConnectionError (EndpointNotSet) -> Thrown if the endpoint does not respond

    RequestError -> Thrown if there is a problem with the request, e. g. invalid parameters
    """
    try:
        endpoint_test = requests.get(f"{endpoint}/@test")

        if endpoint_test.status_code == 200:
            global scans
            scan_id = int(request.args.get('scan_id'))
            host_json = {}
            scan_json = {}
            host_ip = request.args.get('host_ip')

            if scan_id == None: 
                raise RequestError("Scan ID not provided")

            if host_ip:

                for scan in scans:
                    if scan["id"] == scan_id:
                        scan_json = json.loads(scan["scan_json"])

                        single_host_scanned = isinstance(scan_json['host'], dict)

                        if single_host_scanned:

                            host_json = scan_json['host']
                            mac_address_found = not "@addr" in host_json['address']

                        else:
                            hosts = scan_json['host']

                            for host in hosts:

                                mac_address_found = isinstance(host['address'], list)

                                if mac_address_found:
                                    if host['address'][0]['@addr'] == host_ip:
                                        host_json = host
                                        break
                                else:
                                    if host['address']['@addr'] == host_ip:
                                        host_json = host
                                        break
                        break

                if not host_json:  
                    raise RequestError("Invalid Scan ID or Host IP")
                    
            else: 
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
