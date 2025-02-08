import hashlib

def calculate_file_hash(file_path, algorithm="md5"):
    """Calculate the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    
    try:
        with open(file_path, 'rb') as file:
            # Read the file in chunks to avoid memory issues with large files
            while chunk := file.read(8192):  # 8 KB chunks
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error calculating hash: {str(e)}")
