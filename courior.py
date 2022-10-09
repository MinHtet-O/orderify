import random
import threading
import time

def manage_couriers(delivery_queue):
    while True:
        order = delivery_queue.get()
        threading.Thread(target=deliver, args=(order,) ).start()
        if order == None:
            print("All items delivered")
            break

def deliver(order):
    delivery_time = random.randrange(2, 6)
    time.sleep(delivery_time)
    print("Delivered {} after {} seconds \n".format(order.name, delivery_time))