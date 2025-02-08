import re
from datetime import datetime
import json

def load_json_from_string(json_string):
    """
    Load JSON from a string into a Python dictionary.
    
    Args:
        json_string (str): Input JSON string
        
    Returns:
        Dict[str, Any]: Parsed JSON object
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        # Attempt to parse the JSON string
        json_string = json_string.replace('```json', '')
        json_string = json_string.replace('`', '')

        data = json.loads(json_string)
        return data
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {str(e)}")