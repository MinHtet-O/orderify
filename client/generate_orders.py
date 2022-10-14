import time
import requests
import json
from config import API_URL, ORDER_INTERVAL

ORDER_URL = '{}/order'.format(API_URL)
order_file_path = "./resources/orders.json"

def generate_order(orders):
    for order in orders:
        time.sleep(ORDER_INTERVAL)
        resp = requests.post(ORDER_URL, json = order)
        status = resp.status_code
        if status != 200:
            print("Client: {}".format(resp.content))

def load_orders():
    with open(order_file_path) as f:
        orders = json.load(f)
        return orders

def init_order_client():
    orders = load_orders()
    generate_order(orders)
