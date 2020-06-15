import car_monitoring
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

car_monitoring.monitor_car('blabla@gmail.com',
                           '123',
                           '123',
                           '123',
                           '+11123456789',
                           '+33610101010',
                           '111111')
