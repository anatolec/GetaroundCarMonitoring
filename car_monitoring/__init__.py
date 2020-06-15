from .locator import get_location_getaround, get_distance, init_webdriver_with_getaround
from .notif_twilio import send_notif

from time import sleep

__version__ = '1.0.0'

def start_monitoring(getaround_user,
                     getaround_password,
                     twilio_cid,
                     twilio_token,
                     twilio_from,
                     twilio_to,
                     car_id,
                     limit=20,
                     pause=60,
                     headless=True):

    i = 0

    driver = init_webdriver_with_getaround(getaround_user, getaround_password, headless)

    while True:
        lat, lon = get_location_getaround(driver, car_id)

        if i % 2:
            lat1, lon1 = lat, lon
        else:
            lat2, lon2 = lat, lon

        i += 1

        if i < 2:
            continue

        dist_meters = get_distance(lat1, lon1, lat2, lon2)

        print(dist_meters)

        if dist_meters > limit:
            send_notif(twilio_cid,
                       twilio_token,
                       twilio_from,
                       twilio_to,
                       f"Car has moved by {dist_meters} meters !")

        sleep(pause)
