from unicodedata import name
import queue
import threading
from order import *
import time
# TODO: add status field to Order

class Kitchen:
    def __init__(self,order_queue: queue.Queue, delivery_queue: queue.Queue):
        self.orders = dict()
        self.delivery_queue = delivery_queue
        self.order_queue = order_queue
        threading.Thread(target=self.__order_listener).start()
        
    def put_order(self, order):
        self.orders[order.id] = order
        self.order_queue.put(order)
        order.update_status(OrderStatus.ACCEPTED)

    def get_order(self, id):
        return self.orders[id]

    def get_orders(self):
        return self.orders
        
    def __order_listener(self):
        while True:
            order = self.order_queue.get()
            self.__process_order(order)
            
    def __process_order(self, order):
        self.delivery_queue.put(order)
        # put on the shelf
        time.sleep(0)
        print("order "+ order.name+ " is accepted")
        order.update_status(OrderStatus.WAITING)

class InvalidOrderError(Exception):
    pass
    