import random
import threading
import time
from order import *
import requests

# TODO: let courior to know only order id and status
def manage_couriers(delivery_queue):
    while True:
        order = delivery_queue.get()
        threading.Thread(target=deliver, args=(order,) ).start()
        if order == None:
            break

def deliver(order):
    delivery_time = random.randrange(2, 6)
    time.sleep(delivery_time)
    print("Delivered {} after {} seconds \n".format(order.name, delivery_time))
    update_status(order.id, OrderStatus.DELIVERED)

def update_status(order_id, status: OrderStatus):
    # extract the url as const
    url = "http://127.0.0.1:5000/order/{}/status".format(order_id)
    data = dict()
    data['status'] = OrderStatus[status].value
    res = requests.put(url, json = data)
