import queue
import random
import time

from config import API_URL
from order import *
import requests

# TODO: let courior knows only order id and status
class CourierManager:
    def __init__(self, delivery_queue: queue.Queue, min_deliver_duration = 2, max_deliver_duration = 6):
        self.delivery_queue = delivery_queue
        self.__min_delivery_duration = min_deliver_duration
        self.__max_delivery_duration = max_deliver_duration

    def __get_delivery_duration(self) -> int:
        return random.randrange(self.__min_delivery_duration,self.__max_delivery_duration)

    def __spawn_courior(self, order):
        delivery_time = self.__get_delivery_duration()
        time.sleep(delivery_time)
        self.__pickup(order, delivery_time, OrderStatus.DELIVERED)

    def __pickup(self, order, delivery_time, status: OrderStatus):
        status_url = "{}/order/{}/status".format(API_URL, order.id)
        data = dict()
        data['status'] = OrderStatus[status].value
        res = requests.put(status_url, json = data)
        if res.status_code == 200:
            print("Courior: successfully pickedup {} after {} seconds \n".format(order.name, delivery_time))
        else:
            print("Courior: {} {}".format(order.name, res.content))

    def init_manager_thread(self):
        while True:
            order = self.delivery_queue.get()
            print("Courior: {} order received for delivery".format(order.name))
            threading.Thread(target=self.__spawn_courior, args=(order,)).start()

