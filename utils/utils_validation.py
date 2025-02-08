import re
from datetime import datetime
import json

def is_valid_pesel(pesel):
    """Validate PESEL number (11 digits)."""
    if not re.match(r'^\d{11}$', pesel):
        return False
    # Algorithm for PESEL checksum validation
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1]
    total = sum(int(digit) * weight for digit, weight in zip(pesel, weights))
    return total % 10 == 0

def is_valid_regon(regon):
    """Validate REGON number (9 or 14 digits)."""
    if not re.match(r'^\d{9}(\d{5})?$', regon):
        return False
    return True

def is_valid_nip(nip):
    """Validate NIP number (10 digits)."""
    if not re.match(r'^\d{10}$', nip):
        return False
    # NIP checksum algorithm
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    total = sum(int(digit) * weight for digit, weight in zip(nip, weights))
    return total % 11 == int(nip[-1])

def is_valid_date(date_str, date_format="%Y-%m-%d"):
    """Validate and parse date strings into datetime objects."""
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None
def cast_and_validate(data):
    """Cast and validate fields of the data dictionary."""
    
    # Cast to proper types
    if 'wysokosc skladki' in data and data['wysokosc skladki']:
        data['wysokosc skladki'] = float(data['wysokosc skladki'])
    
    # Validate PESEL/REGON and NIP
    if 'PESEL/REGON' in data:
        pesel_regon = data['PESEL/REGON']
        if len(pesel_regon) == 11:
            if not is_valid_pesel(pesel_regon):
                raise ValueError(f"Invalid PESEL: {pesel_regon}")
        elif len(pesel_regon) == 9 or len(pesel_regon) == 14:
            if not is_valid_regon(pesel_regon):
                raise ValueError(f"Invalid REGON: {pesel_regon}")
        else:
            raise ValueError(f"Invalid PESEL/REGON: {pesel_regon}")
    
    if 'dane ubezpieczajacego' in data and 'NIP' in data['dane ubezpieczajacego']:
        nip = data['dane ubezpieczajacego']['NIP']
        if not is_valid_nip(nip):
            raise ValueError(f"Invalid NIP: {nip}")
    
    # Validate other fields if needed
    # For example: validate dates, check for required fields, etc.
    
    return data

def load_json_from_string(json_string):
    """Load JSON from a string and validate it."""
    try:
        # Attempt to parse the JSON string
        data = json.loads(json_string)
        
        # Perform additional structure checks (optional)
        if not isinstance(data, dict):
            raise ValueError("JSON must be a dictionary.")
        
        # Here you can check if essential keys exist
        required_keys = [
            "dane ubezpieczonego", "dane ubezpieczajacego", "dane przedmiotu ubezpieczenia",
            "wysokosc skladki", "forma platnosci", "raty", "ilosc przyjetej gotowki",
            "marka towarzystwa ubezpieczeniowego", "kategoria polisy"
        ]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        
        return data
    
    except json.JSONDecodeError as e:
        # Return a detailed error message if JSON is invalid
        raise ValueError(f"Invalid JSON string: {str(e)}")
    except ValueError as ve:
        # Catch any validation errors
        raise ve
