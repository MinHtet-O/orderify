from time import sleep
import queue, threading, json
from flask import Flask, jsonify, request
from courior.courior import CourierManager
from kitchen.kitchen import Kitchen
from shelf_manager.shelf_manager import ShelfManager
from client.generate_orders import init_order_client
from order.order import OrderStatus, OrderEncoder
from pickup_area.pickup_area import *
from config import CLOCK_INTERVAL, allowable_shelf_size, MAX_DELIVER_DURATION, MIN_DELIVER_DURATION
from errors import InvalidOrderError, InvalidOrderStatus
from consts import *

# TODO: add type annotation in all methods
# init events
manage_shelf_event = threading.Event()

def tick_events():
    while True:
        sleep(CLOCK_INTERVAL)
        manage_shelf_event.set()

# init pickup area
pickup_area = PickupArea()
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.HOT)
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.COLD)
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.FROZEN)
pickup_area.add_overflow_shelf(allowable_shelf_size)

shelf_manager = ShelfManager()
managed_pickup_area = shelf_manager.assign(pickup_area= pickup_area)

# init kitchen
delivery_queue = queue.Queue()
kitchen = Kitchen(
    delivery_queue = delivery_queue,
    pickup_area= managed_pickup_area
)

# init courior manager
courior_manager = CourierManager(
    delivery_queue,
    min_deliver_duration=MIN_DELIVER_DURATION,
    max_deliver_duration=MAX_DELIVER_DURATION
)

# init threads
threading.Thread(target=courior_manager.init_manager_thread).start()
threading.Thread(target=shelf_manager.manage_shelves, args=(manage_shelf_event,)).start()
threading.Thread(target=init_order_client).start()
threading.Thread(target=tick_events).start()

# init API server
app = Flask(__name__)
@app.route('/order',methods = ['POST'])
def post_order():
    try:
        json = request.get_json()
        order = Order.decode_json(json)
        kitchen.put_order(order)
    except InvalidOrderError as e:
        return "Invalid order: {msg}".format(msg = e), HTTP_STATUS_INTERNAL_ERROR
    except NoEmptySpaceErr as e:
        return '{}'.format(e), HTTP_STATUS_INTERNAL_ERROR
    except Exception as e:
        return 'unknown error {}', HTTP_STATUS_INTERNAL_ERROR
    return order.id, HTTP_STATUS_OK

@app.route('/order/<string:id>/status',methods = ['PUT'])
def update_order_status(id):
    try:
        json = request.get_json()
        status = OrderStatus.decode_json(json)
        kitchen.update_order_status(id, status)
    except InvalidOrderID as e:
        return "invalid order id: {}".format(e), HTTP_STATUS_INTERNAL_ERROR
    except InvalidOrderStatus as e:
        return "invalid order status: {}".format(e), HTTP_STATUS_INTERNAL_ERROR
    # except Exception as e:
    #     return "unknown error", HTTP_STATUS_INTERNAL_ERROR
    return '',HTTP_STATUS_OK

@app.route('/order/<string:id>/',methods = ['GET'])
def get_order(id):
    try:
        order = kitchen.get_order(id)
    except InvalidOrderID as e:
        return "invalid order id: {}".format(e), HTTP_STATUS_INTERNAL_ERROR
    except Exception as e:
        return "unknown error", HTTP_STATUS_INTERNAL_ERROR
    return json.dumps(order, indent=4, cls=OrderEncoder), HTTP_STATUS_OK

if __name__ == "__main__":
    app.run(debug=False)

# TODO: add logger for both debug and info
# TODO: response error json response for API end points
