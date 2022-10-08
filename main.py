import threading
import queue
import time

order_queue = queue.Queue()
delivery_queue = queue.Queue()

def kitchen():
    while True:
        item = order_queue.get()
        delivery_queue.put(item)
        if item == None:
            print("About to Close")
            break
        print(f'Cooking on {item}')

def courier():
    while True:
        item = delivery_queue.get()
        if item == None:
            print("All items delivered")
            break
        print(f'Delivering on {item}')

def order():
    for item in range(10):
        order_queue.put(item)
        time.sleep(0.5)
    order_queue.put(None)

threading.Thread(target=kitchen).start()
threading.Thread(target=courier).start()
threading.Thread(target=order).start()

print('All items processed')