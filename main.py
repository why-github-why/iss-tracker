from datetime import datetime
import requests
from smtplib import SMTP
import time

EMAIL = "smtplib2@gmail.com"
PASSWORD = "smtpL18#!"
LATITUDE = -29.119994
LONGITUDE = 26.229913


def is_night():
    response = requests.get(f"https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}")
    response.raise_for_status()

    data = response.json()
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    # Convert 12-hour to 24-hour time
    sunset_24 = ""
    if sunset[-2:] == "PM":
        hour = str(int(sunset[0]) + 12)
        sunset_24 = hour + sunset[1:]

    now = datetime.now()
    current_hour_24 = now.strftime("%H")
    if int(current_hour_24) >= int(sunset_24[:2]) or int(current_hour_24) <= int(sunrise[:1]):
        return True


def is_iss_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_data = iss_response.json()
    iss_latitude = float(iss_data['iss_position']['latitude'])
    iss_longitude = float(iss_data['iss_position']['longitude'])

    if LATITUDE-5 <= iss_latitude <= LATITUDE+5 and LONGITUDE-5 <= iss_longitude <= LONGITUDE+5:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        server = SMTP("smtp.gmail.com")
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you!☄️"
        )

# print(f"Sunrise: {sunrise}\n"
#       f"Sunset(12hr): {sunset}\n"
#       f"Sunset(24hr): {sunset_24}")

# day = now.strftime("%A")
# day_of_month = now.strftime("%d")
# month = now.strftime("%m")
# year = now.strftime("%Y")
# print(f"Date: {day}, {day_of_month}/{month}/{year}\n")

# from math import floor
# print(abs(floor(LATITUDE)), floor(LONGITUDE), floor(iss_latitude), abs(floor(iss_longitude)))
# lat_diff = abs(floor(LATITUDE) - floor(iss_latitude))
# lng_diff = abs(floor(LONGITUDE) - floor(iss_longitude))
# print(lat_diff, lng_diff)
# if 5 > lat_diff > 0 and 5 > lng_diff > 0:
#     pass

# import urllib.request as url
# import json
#
# request = url.Request("http://api.open-notify.org/iss-now.json")
# response = url.urlopen(request)
# print(response.getcode())
#
# data = json.loads(response.read())
# print(type(data), data)
# latitude = data['iss_position']['latitude']
# longitude = data['iss_position']['longitude']
# print(f"\nCurrent ISS location"
#       f"\n--------------------"
#       f"\nLatitude: {latitude}"
#       f"\nLongitude: {longitude}")
