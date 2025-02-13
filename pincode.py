import requests
import re
from thefuzz import fuzz, process

def extract_pincode(address):
    match = re.search(r'\b\d{6}\b', address)
    return match.group() if match else None

def extract_post_office(address):
    """Extract potential post office names from address"""
    keywords = ['colony', 'nagar', 'bank']
    parts = [part.strip() for part in address.lower().split(',')]
    post_offices = []
    
    for part in parts:
        # Check if part contains any keywords
        if any(keyword in part.lower() for keyword in keywords):
            post_offices.append(part.strip())
    
    return post_offices

def normalize_address(address):
    """Normalize address by handling common variations"""
    address = address.lower()
    address = re.sub(r'\bbengaluru\b', 'bangalore', address)
    address = re.sub(r'\brd\b', 'road', address)
    address = re.sub(r'\bst\b', 'street', address)
    return address

def get_pincode_details(pincode):
    """Get details from pincode API"""
    try:
        response = requests.get(f"https://api.postalpincode.in/pincode/{pincode}")
        data = response.json()
        if data and data[0]['Status'] == "Success":
            return data[0]['PostOffice']
        return None
    except:
        return None

def get_post_office_details(post_office):
    """Get details from post office API"""
    try:
        response = requests.get(f"https://api.postalpincode.in/postoffice/{post_office}")
        data = response.json()
        if data and data[0]['Status'] == "Success":
            return data[0]['PostOffice']
        return None
    except:
        return None

def fuzzy_match_post_office(post_office_name, valid_names, threshold=70):
    """Check if post office name matches any valid names using fuzzy matching"""
    if not valid_names:
        return False
    best_match, score = process.extractOne(post_office_name, valid_names, scorer=fuzz.token_sort_ratio)
    return score >= threshold

def validate_address(address):
    """Validate address using both PIN code and Post Office APIs"""
    if not address or len(address.strip()) < 10:
        return "Invalid address: Address too short"

    # Extract PIN code
    pincode = extract_pincode(address)
    if not pincode:
        return "Invalid address: No PIN code found"

    # Get PIN code details
    pin_details = get_pincode_details(pincode)
    if not pin_details:
        return "Invalid PIN code: No data found"

    # Extract and validate post office names
    post_offices = extract_post_office(address)
    if not post_offices:
        return "Invalid address: No post office or locality found"

    # Normalize address for comparison
    normalized_address = normalize_address(address)

    # Collect valid information from PIN code API
    valid_state = pin_details[0]['State'].lower()
    valid_district = pin_details[0]['District'].lower()
    valid_areas = {po['Name'].lower() for po in pin_details}
    valid_regions = {po['Region'].lower() for po in pin_details}
    
    # Validate state and district
    if valid_state not in normalized_address:
        return f"Invalid address: State mismatch. Expected {valid_state.title()}"
    
    if valid_district not in normalized_address and 'bangalore' not in normalized_address:
        return f"Invalid address: District mismatch. Expected {valid_district.title()}"

    # Cross-validate with post office API
    post_office_validated = False
    for po_name in post_offices:
        po_details = get_post_office_details(po_name)
        if po_details:
            # Check if any returned post office matches the PIN code
            for po in po_details:
                if po['Pincode'] == pincode:
                    post_office_validated = True
                    break
        
        # If API validation fails, try fuzzy matching with known valid areas
        if not post_office_validated:
            if fuzzy_match_post_office(po_name, valid_areas) or fuzzy_match_post_office(po_name, valid_regions):
                post_office_validated = True

    if not post_office_validated:
        return "Invalid address: Post office/locality doesn't match PIN code"

    # Additional validation for 560050
    if pincode == '560050':
        required_areas = ['banashankari', 'srinivasa nagar']
        for area in required_areas:
            if area not in normalized_address:
                return f"Invalid address: Missing required area '{area.title()}' for 560050"

    return "Valid address"

def test_addresses():
    address = input("enter the address: ")
    print(f"\nAddress: {address}")
    print(f"Validation: {validate_address(address)}")

if __name__ == "__main__":
    test_addresses()