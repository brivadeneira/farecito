"""
Pipeline utils
"""
from geopy.geocoders import Nominatim


def city_to_country_code_and_flag(city_name: str) -> str:
    """
    Gen the correspondant country flag emoji, given the city name

    :param city_name: (str) e.g. 'Lisbon'
    :return: (str) country code and flag emoji e.g. 'PT 🇵🇹'
    """
    geolocator = Nominatim(user_agent="city-country-lookup")
    location = geolocator.geocode(city_name)

    if not location:
        raise ValueError(f"{city_name} can not be localized.")

    locator = geolocator.reverse((location.latitude, location.longitude))
    country_code = locator.raw["address"]["country_code"].upper()

    flag = ""
    for char in country_code:
        flag += chr(127397 + ord(char))

    return f"{country_code} {flag}"
