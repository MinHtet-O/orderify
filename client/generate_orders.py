import time
import requests
import json

url = 'http://127.0.0.1:5000/order'
order_file_path = "./resources/orders.json"

def generate_order(orders):
    for order in orders:
        time.sleep(0.1)
        x = requests.post(url, json = order)
        print(x)

def load_orders():
    with open(order_file_path) as f:
        orders = json.load(f)
        return orders

def init_order_client():
    # wait for the kitchen to start receiving the orders
    time.sleep(2)
    orders = load_orders()
    generate_order(orders)
