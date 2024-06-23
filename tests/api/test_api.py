import pytest
# import json
from FlightRadar24 import FlightRadar24API


@pytest.mark.change
def test_remove_name(user):
    user.name = ''
    assert user.name == ''


@pytest.mark.check
def test_name(user):
    assert user.name == 'Sergii'


@pytest.mark.check
def test_second_name(user):
    assert user.second_name == 'Butenko'


@pytest.mark.fr
def test_functions():
    all_functions = dir(FlightRadar24API)
    print(all_functions)
    help(FlightRadar24API.get_flight_details)


def convert_unix_to_hms(seconds):
    # Check if the difference is negative
    is_negative = seconds < 0
    # Work with the absolute value of seconds
    seconds = abs(seconds)
    
    # Calculate the number of hours, minutes, and remaining seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    # Format the time as HH:MM:SS
    hms_format = f"{int(hours):02}:{int(minutes):02}:{int(remaining_seconds):02}"
    
    # Add a negative sign if the original difference was negative
    if is_negative:
        hms_format = "-" + hms_format
    
    return hms_format
    
    
@pytest.mark.fr    
def test_arrival_time_difference():
    fr_api = FlightRadar24API()
    airport_code = 'FAO'
    airport_details = fr_api.get_airport_details(airport_code)
    arrivals_data = airport_details['airport']['pluginData']['schedule']['arrivals']['data']
    flight_tracker = ['FR3519']
    
    for arrival in arrivals_data:
        flight_number = arrival['flight']['identification']['number']['default']
        scheduled_arrival = arrival['flight']['time']['scheduled']['arrival']
        estimated_arrival = arrival['flight']['time']['estimated']['arrival']
        
        if flight_number in flight_tracker:
            if estimated_arrival is not None:            
                print(f"{flight_number} arrives {convert_unix_to_hms(estimated_arrival-scheduled_arrival)} of schedule")
            else:
                print(f"{flight_number} not departed yet.")
        
  
    # formatted_data = json.dumps(arrivals_data, indent=4) 
    # with open('flight_details.json', 'w') as file:
        # file.write(formatted_data)
