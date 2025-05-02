import re

# Define coordinates in organized dictionaries
table_rows = [0, 85, 130, 180, 228, 270, 320, 365, 413, 455, 503, 550,
              595, 640, 690, 735, 784, 830, 871, 924, 972, 1017, 1064, 1110]

table_cols = [
    0, 95, 173, 257, 340, 420, 504, 581, 662, 747, 825, 905, 
    988, 1070, 1150, 1232, 1312, 1398, 1475, 1549, 1630
]

def dms_to_decimal(degrees, minutes, direction):
    """Convert degrees, minutes, and direction to decimal degrees."""
    if minutes == '':
        minutes = 0
    decimal = float(degrees) + float(minutes)/60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def parse_coordinates(coord_str):
    """Parse coordinate string into latitude and longitude."""
    # Grab the relevant part of the string (latitude and longitude only)
    match = re.match(r'(\d+)[°′\'](\d{0,2})[°′\']{0,1}(N),\s*(\d+)[°′\'](\d{0,2})[°′\']{0,1}(E)', coord_str)
    if not match:
        raise ValueError("Invalid coordinate format")
    
    lat_deg, lat_decimals, lat_dir, lon_deg, lon_decimals, lon_dir = match.groups()
    
    if lat_decimals != '':
        latitude = float(lat_deg) + float(lat_decimals) / 10
    else:
        latitude = float(lat_deg)
    
    if lon_decimals != '':
        longitude = float(lon_deg) + float(lon_decimals) / 10
    else:
        longitude = float(lon_deg)
    
    return latitude, longitude 