from courior.courior import *
from config import *
from kitchen.kitchen import *
from flask import Flask, jsonify, request
from client.generate_orders import *
from consts import *
from shelf_manager.shelf_manager import *
# consts

# init events
shef_managment_event = threading.Event()

def tick_events():
    while True:
        time.sleep(CLOCK_INTERVAL)
        shef_managment_event.set()


# init shelf manager
shelf_manager = ShelfManager()
shelf_manager.add_allowable_shelf(allowable_shelf_size, Temp.HOT)
shelf_manager.add_allowable_shelf(allowable_shelf_size, Temp.COLD)
shelf_manager.add_allowable_shelf(allowable_shelf_size, Temp.FROZEN)
shelf_manager.add_overflow_shelf(allowable_shelf_size)

# init kitchen
delivery_queue = queue.Queue()
kitchen = Kitchen(delivery_queue, shelf_manager)

# init courior manager
courior_manager = CourierManager(
    delivery_queue,
    min_deliver_duration=MIN_DELIVER_DURATION,
    max_deliver_duration=MAX_DELIVER_DURATION)

# init threads
threading.Thread(target=courior_manager.init_manager_thread).start()
threading.Thread(target=shelf_manager.init_manager_thread, args=(shef_managment_event,)).start()
threading.Thread(target=init_order_client).start()
threading.Thread(target=tick_events).start()

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
        return 'unknown error', HTTP_STATUS_INTERNAL_ERROR
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
    except Exception as e:
        return "unknown error", HTTP_STATUS_INTERNAL_ERROR
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

@app.route('/order',methods = ['GET'])
def get_orders():
    try:
        orders = kitchen.get_orders()
    except Exception as e:
        return "unknown error", HTTP_STATUS_INTERNAL_ERROR
    return jsonify(
                    data=json.dumps(orders, indent=4),
                    status=HTTP_STATUS_OK
                )

if __name__ == "__main__":
    app.run(debug=False)

# TODO: add logger for both debug and info
# TODO: response error json response for end points
