import json
from datetime import datetime
from typing import Dict, Union, List, Any

def process_to_JSON(llm_string: str) -> Dict[str, Any]:
    """
    Process, validate, and format JSON string from LLM output.
    
    Args:
        llm_string (str): JSON string from LLM
        
    Returns:
        Dict[str, Any]: Validated and formatted JSON object
        
    Raises:
        ValueError: If JSON is invalid or validation fails
    """
    try:
        # First, load and validate basic JSON structure
        data = load_json_from_string(llm_string)
        
        # Cast and validate standard fields
        data = cast_and_validate(data)
        
        # Process specific field types
        if 'dane przedmiotu ubezpieczenia' in data:
            przedmiot = data['dane przedmiotu ubezpieczenia']
            
            # Handle rocznik (integer or None)
            if 'rocznik' in przedmiot:
                if przedmiot['rocznik']:
                    try:
                        przedmiot['rocznik'] = int(przedmiot['rocznik'])
                    except (ValueError, TypeError):
                        raise ValueError(f"Invalid rocznik value: {przedmiot['rocznik']}")
                        
            # Address can be None for non-building insurance
            if 'adres' in przedmiot and not przedmiot['adres']:
                przedmiot['adres'] = None
        
        # Process payment information
        if 'wysokosc skladki' in data:
            if data['wysokosc skladki']:
                try:
                    data['wysokosc skladki'] = float(data['wysokosc skladki'])
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid wysokosc skladki: {data['wysokosc skladki']}")
        
        if 'raty' in data:
            if 'wysokosci rat' in data['raty']:
                if data['raty']['wysokosci rat']:
                    try:
                        data['raty']['wysokosci rat'] = [
                            float(rata) for rata in data['raty']['wysokosci rat']
                        ]
                    except (ValueError, TypeError):
                        raise ValueError("Invalid wysokosci rat values")
                else:
                    data['raty']['wysokosci rat'] = None
            
            if 'daty platnosci rat' in data['raty']:
                if data['raty']['daty platnosci rat']:
                    validated_dates = []
                    for date_str in data['raty']['daty platnosci rat']:
                        validated_date = is_valid_date(date_str)
                        if not validated_date:
                            raise ValueError(f"Invalid date format: {date_str}")
                        validated_dates.append(date_str)  # Keep original string format
                    data['raty']['daty platnosci rat'] = validated_dates
                else:
                    data['raty']['daty platnosci rat'] = None
        
        if 'ilosc przyjetej gotowki' in data:
            if data['ilosc przyjetej gotowki']:
                try:
                    data['ilosc przyjetej gotowki'] = float(data['ilosc przyjetej gotowki'])
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid ilosc przyjetej gotowki: {data['ilosc przyjetej gotowki']}")
            else:
                data['ilosc przyjetej gotowki'] = None
        
        # Validate payment consistency
        if data.get('forma platnosci') != 'raty' and data['raty'].get('wysokosci rat'):
            raise ValueError("Payment installments specified but forma platnosci is not 'raty'")
        
        if data.get('forma platnosci') != 'gotowka' and data.get('ilosc przyjetej gotowki'):
            raise ValueError("Cash amount specified but forma platnosci is not 'gotowka'")
        
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing JSON: {str(e)}")

if __name__ == "__main__":
    # Example
    try:
        processed_json = process_to_JSON(llm_string)
        print("Successfully processed JSON:", processed_json)
    except ValueError as e:
        print("Error processing JSON:", str(e))

