import time

def order(order_queue):
    for item in range(10):
        order_queue.put(item)
        time.sleep(0.5)
    order_queue.put(None)