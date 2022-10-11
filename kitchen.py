from unicodedata import name
import queue
import threading
from order import *
import time
from shelf_manager import *
# TODO: add status field to Order

class Kitchen:
    def __init__(self,order_queue: queue.Queue, delivery_queue: queue.Queue, shelf_manager: ShelfManager):
        self.orders = dict()
        self.delivery_queue = delivery_queue
        self.order_queue = order_queue
        self.shelf_manager = shelf_manager
        threading.Thread(target=self.__order_listener).start()

    def update_order_status(self, id: string, status: OrderStatus):
        if id not in self.orders:
            raise InvalidOrderID("order id {} not exists".format(id))
        order = self.orders[id]
        if (order.status == OrderStatus.FAILED) and (status != OrderStatus.FAILED):
            raise InvalidOrderStatus("order id {} has already failed".format(id))
        order.update_status(status)

    def put_order(self, order: Order):
        self.orders[order.id] = order
        self.shelf_manager.put_order(order)
        self.order_queue.put(order)
        order.update_status(OrderStatus.ACCEPTED)

    def get_order(self, id):
        if id not in self.orders.keys():
            raise InvalidOrderID("order id {} not exists".format(id))
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
        print("LEN {}".format(len(self.orders)))

# TODO: refactor all exceptions in the single folder
class InvalidOrderError(Exception):
    pass

class InvalidOrderID(Exception):
    pass


#test: update the order status of failed order
#expected: raise error
