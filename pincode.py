import requests
import re
from thefuzz import fuzz, process

def extract_pincode(address):
    """Extract 6-digit PIN code from address"""
    # Handle addresses without spaces
    if not ' ' in address:
        match = re.search(r'\d{6}', address)
        return match.group() if match else None
    
    match = re.search(r'\b\d{6}\b', address)
    return match.group() if match else None

def normalize_address(address):
    """Normalize address by handling common variations"""
    # Handle addresses without spaces
    if not ' ' in address:
        # Add space before capital letters
        address = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
    
    address = address.lower()
    # City name variations
    address = re.sub(r'\bbengaluru\b', 'bangalore', address)
    address = re.sub(r'\bgurgaon\b', 'gurugram', address)
    address = re.sub(r'\bbombay\b', 'mumbai', address)
    # Common abbreviations
    address = re.sub(r'\brd\b', 'road', address)
    address = re.sub(r'\bst\b', 'street', address)
    address = re.sub(r'\bapt\b', 'apartment', address)
    return address

def get_pincode_details(pincode):
    """Get details from pincode API with error handling"""
    try:
        response = requests.get(f"https://api.postalpincode.in/pincode/{pincode}", timeout=5)
        data = response.json()
        if data and data[0]['Status'] == "Success":
            return data[0]['PostOffice']
        return None
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

def extract_locality(address):
    """Extract locality information from address using common Indian address patterns"""
    # Split address into parts
    if not ' ' in address:
        address = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
    
    parts = [part.strip() for part in re.split(r'[,\s]+', address) if part.strip()]
    
    # Common locality indicators
    locality_indicators = [
        'sector', 'phase', 'block', 'layout', 'nagar', 'colony', 'garden', 'park',
        'complex', 'apartment', 'tower', 'hills', 'estate', 'market', 'place',
        'road', 'street', 'lane', 'area', 'district', 'zone', 'extension', 'enclave'
    ]
    
    localities = []
    for i, part in enumerate(parts):
        part_lower = part.lower()
        # Check if part contains locality indicators
        if any(indicator in part_lower for indicator in locality_indicators):
            # Include the previous part if it exists (e.g., "DLF Phase")
            if i > 0:
                localities.append(f"{parts[i-1]} {part}")
            else:
                localities.append(part)
        # Check for standalone names that are likely localities
        elif len(part) > 3 and part.isalpha():
            localities.append(part)
    
    return localities

def validate_address(address):
    """Validate Indian addresses"""
    if not address or len(address.strip()) < 5:
        return "Invalid address: Address too short"

    # Extract PIN code
    pincode = extract_pincode(address)
    if not pincode:
        return "Invalid address: No PIN code found"

    # Get PIN code details
    pin_details = get_pincode_details(pincode)
    if not pin_details:
        return "Invalid PIN code: No data found"

    # Normalize address
    normalized_address = normalize_address(address)
    
    # Extract localities
    localities = extract_locality(address)
    if not localities:
        localities = [part.strip() for part in address.split(',') if len(part.strip()) > 3]

    # Get valid information from PIN code
    valid_state = pin_details[0]['State'].lower()
    valid_district = pin_details[0]['District'].lower()
    
    # Collect all valid areas from PIN code data
    valid_areas = set()
    for po in pin_details:
        valid_areas.add(po['Name'].lower())
        valid_areas.add(po['Region'].lower())
        if po.get('Division'):
            valid_areas.add(po['Division'].lower())
        if po.get('Area'):
            valid_areas.add(po['Area'].lower())

    # State validation with flexible matching
    state_found = False
    if valid_state in normalized_address:
        state_found = True
    else:
        # Handle special cases like "Delhi" vs "New Delhi"
        if valid_state == "delhi" and ("delhi" in normalized_address or "new delhi" in normalized_address):
            state_found = True
    
    if not state_found:
        return f"Invalid address: Expected state {valid_state.title()}"

    # District/City validation with flexible matching
    district_found = False
    if valid_district in normalized_address:
        district_found = True
    else:
        # Handle common city variations
        common_cities = {
            "delhi": ["new delhi", "south delhi", "north delhi"],
            "mumbai": ["bombay"],
            "bangalore": ["bengaluru"],
            "gurugram": ["gurgaon"]
        }
        if valid_district.lower() in common_cities:
            district_found = any(city in normalized_address for city in common_cities[valid_district.lower()])
    
    # Area/Locality validation
    locality_found = False
    for locality in localities:
        # Direct match with valid areas
        if locality.lower() in valid_areas:
            locality_found = True
            break
        # Fuzzy match with valid areas
        best_match, score = process.extractOne(locality.lower(), valid_areas, scorer=fuzz.token_sort_ratio)
        if score >= 70:  # Threshold for fuzzy matching
            locality_found = True
            break
    
    if not locality_found:
        # More lenient validation for major cities
        major_cities = ["delhi", "mumbai", "bangalore", "kolkata", "chennai", "hyderabad", "pune", "gurugram"]
        if any(city in normalized_address for city in major_cities):
            locality_found = True

    if not locality_found:
        return "Address validated with PIN code but locality not recognized"

    return "Valid address"

def test_addresses():
    address=input("Enter the address: ")
    print(f"\nAddress: {address}")
    print(f"Validation: {validate_address(address)}")

if __name__ == "__main__":
    test_addresses()