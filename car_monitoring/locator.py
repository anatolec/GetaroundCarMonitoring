import logging
import requests
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)

def get_location_getaround(user, password, car_id):
    try:
        session = requests.session()

        response = session.get('https://fr.getaround.com/login')

        soup = BeautifulSoup(response.text, features="html.parser")

        token = soup.find("input", {"name": "authenticity_token"}).attrs['value']

        data = {"authenticity_token": token,
                #"commit": "Se connecter",
                "user[email]": user,
                "user[password]": password,
                #"user[remember_me]": 1
                }

        session.post('https://fr.getaround.com/login', data=data)

        soup = BeautifulSoup(
            json.loads(session.get(f'https://fr.getaround.com/dashboard/cars/{car_id}/open_management/status').text)['html'],
            features="html.parser")

        google_maps_url = soup.find("a", {"target": "_blank"}).attrs['href']

        lat, long = extract_coordinage(google_maps_url)
    except TypeError:
        return 0, 0
    return lat, long


def get_location_getaround_selenium(driver, car_id):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get(f"https://fr.getaround.com/dashboard/cars/{car_id}/open_management")

    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@target='_blank']")))

    google_maps_url = element.get_attribute('href')

    lat, long = extract_coordinage(google_maps_url)

    return lat, long

def extract_coordinage(google_maps_url):
    lat, long = google_maps_url.split('=')[2].split('%2C')

    lat = float(lat)
    long = float(long)

    return lat, long

def get_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000

    return distance


def init_selenium_with_getaround(user, password, headless=True):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    import chromedriver_autoinstaller

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1280")

    if headless:
        chrome_options.add_argument('headless')

    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f"https://fr.getaround.com/dashboard/cars/0/open_management")

    driver.find_element_by_xpath("//input[@name='user[email]']").send_keys(user)
    driver.find_element_by_xpath("//input[@name='user[password]']").send_keys(password)

    driver.find_element_by_xpath("//input[@name='commit']").click()

    return driver
