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

    Returns
    -------
    None

    Exceptions
    ----------
    OperationalError -> Thrown if there is a database malfunction
    """    
    try:
        xml_content = subprocess.getoutput(f"nmap -oX - {options} {range}") # Run the scan and create an XML
        data_dict = xmltodict.parse(xml_content)    # Convert the XML to dict

        json_output = data_dict['nmaprun']
        json_output = json.dumps(json_output)   # Convert the dict to JSON
                
        new_scan = Scan(name=scan_type, target=range, scan_json=json_output)    
        db.session.add(new_scan)
        db.session.commit()
    
    except Exception as e:
        handle_error(e)
