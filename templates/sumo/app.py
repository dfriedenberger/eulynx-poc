import threading
import logging
import os
import time

from webapp import WebPage
from traciapp import Simulation


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    simulation = Simulation("sumo")

    webpage = WebPage("flask",simulation.commands)


    threading.Thread(target=webpage.run).start()
    threading.Thread(target=simulation.run).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("CTRL+C called")
    os._exit(1)



