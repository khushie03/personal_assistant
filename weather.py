import pyowm

owm = pyowm.OWM('your_api_key')  

def weather_info(location):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)
    weather = observation.weather
    
    temperature_fahrenheit = weather.temperature('fahrenheit')['temp']
    description = weather.detailed_status
    
    return temperature_fahrenheit, description
