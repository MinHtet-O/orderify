import threading
import queue
from order.order import *
from flask import Flask

# order_queue = queue.Queue()
# delivery_queue = queue.Queue()

# def kitchen():
#     while True:
#         item = order_queue.get()
#         delivery_queue.put(item)
#         if item == None:
#             print("About to Close")
#             break
#         print(f'Cooking on {item}')

# def courier():
#     while True:
#         item = delivery_queue.get()
#         if item == None:
#             print("All items delivered")
#             break
#         print(f'Delivering on {item}')



# threading.Thread(target=kitchen).start()
# threading.Thread(target=courier).start()
# threading.Thread(target=order, args=(order_queue, )).start()

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
