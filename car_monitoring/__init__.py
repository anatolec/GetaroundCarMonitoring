from .locator import get_location_getaround, get_distance
from .notif_twilio import send_notif

import logging

from time import sleep

__version__ = '1.0.0'

__all__ = ['monitor_car', 'get_location_getaround']

logger = logging.getLogger(__name__)


def monitor_car(getaround_user,
                getaround_password,
                twilio_cid,
                twilio_token,
                twilio_from,
                twilio_to,
                car_id,
                limit=20,
                pause=60,
                stop_when_move=False):

    i = 0

    while True:
        lat, lon = get_location_getaround(getaround_user, getaround_password, car_id)

        if (lat, lon) == (0, 0):
            logger.info("Location failed")
            sleep(pause)
            continue

        logger.info(f"Car located at {lat}, {lon}")

        if i % 2:
            lat1, lon1 = lat, lon
        else:
            lat2, lon2 = lat, lon

        i += 1

        if i < 2:
            continue

        dist_meters = get_distance(lat1, lon1, lat2, lon2)

        logger.info(f"Distance with latest location = {dist_meters} m")

        if dist_meters > limit:
            send_notif(twilio_cid,
                       twilio_token,
                       twilio_from,
                       twilio_to,
                       f"Car has moved by {int(dist_meters)} meters ! Latest position at = "
                       f"https://www.google.com/maps/search/?api=1&query={lat},{lon}")

            if stop_when_move:
                break

        sleep(pause)
