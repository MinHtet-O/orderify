import json
import queue
import threading
from time import sleep

from flask import Flask, request

from client.generate_orders import init_order_client
from config import allowable_shelf_size, MAX_DELIVER_DURATION, MIN_DELIVER_DURATION
from consts import *
from courior.courior import CourierManager
from errors import InvalidOrderError, InvalidOrderStatus
from kitchen.kitchen import Kitchen
from order.order import OrderStatus, OrderEncoder
from pickup_area.pickup_area import *
from shelf_policy import ShelfPolicyAggregator, OrderDeteriorator, SpoiledOrderRemover, OnFullOrderRemover, \
    OrderRelocator

# init pickup area
pickup_area = PickupArea()
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.HOT)
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.COLD)
pickup_area.add_allowable_shelf(allowable_shelf_size, Temp.FROZEN)
pickup_area.add_overflow_shelf(allowable_shelf_size)

# init shelf policies
shelf_policies = ShelfPolicyAggregator(
    OrderDeteriorator(),
    SpoiledOrderRemover(),
    OnFullOrderRemover(),
    OrderRelocator()
)
# init kitchen
delivery_queue = queue.Queue()
kitchen = Kitchen(
    delivery_queue=delivery_queue,
    pickup_area=pickup_area
)

# init courior manager
courior_manager = CourierManager(
    delivery_queue,
    min_deliver_duration=MIN_DELIVER_DURATION,
    max_deliver_duration=MAX_DELIVER_DURATION
)

# init threads
threading.Thread(target=courior_manager.init_manager_thread).start()
threading.Thread(target=shelf_policies.apply_per_interval, args=(pickup_area,)).start()
threading.Thread(target=init_order_client).start()

# init API server
app = Flask(__name__)


@app.route('/order', methods=['POST'])
def post_order():
    try:
        req_json = request.get_json()
        order = Order.decode_json(req_json)
        kitchen.put_order(order)
    except InvalidOrderError as e:
        return f"Invalid order: {str(e)}", HTTP_STATUS_INTERNAL_ERROR
    except NoEmptySpaceErr as e:
        return f"{str(e)}", HTTP_STATUS_INTERNAL_ERROR
    except Exception as e:
        return 'unknown error {}', HTTP_STATUS_INTERNAL_ERROR
    return order.id, HTTP_STATUS_OK


@app.route('/order/<string:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        json_data = request.get_json()
        status = OrderStatus.decode_json(json_data)
        kitchen.update_order_status(order_id, status)
    except InvalidOrderID as e:
        return f"invalid order id: {str(e)}", HTTP_STATUS_INTERNAL_ERROR
    except InvalidOrderStatus as e:
        return f"invalid order status: {str(e)}", HTTP_STATUS_INTERNAL_ERROR
    # except Exception as e:
    #     return "unknown error", HTTP_STATUS_INTERNAL_ERROR
    return '', HTTP_STATUS_OK


@app.route('/order/<string:id>/', methods=['GET'])
def get_order(order_id):
    try:
        order = kitchen.get_order(order_id)
    except InvalidOrderID as e:
        return f"invalid order id: {str(e)}", HTTP_STATUS_INTERNAL_ERROR
    except Exception as e:
        return "unknown error", HTTP_STATUS_INTERNAL_ERROR
    return json.dumps(order, indent=4, cls=OrderEncoder), HTTP_STATUS_OK


if __name__ == "__main__":
    app.run(debug=False)

# TODO: add logger for both debug and info
# TODO: response error json response for API end points
