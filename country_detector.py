import pycountry

def detect_country(text):

    text = text.lower()

    for country in pycountry.countries:

        if country.name.lower() in text:
            return country.name

    return "Unknown"