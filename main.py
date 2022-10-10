import threading
import queue
from order import *
from courior import *
from kitchen import *
from flask import Flask, jsonify, request
from client.generate_orders import *

delivery_queue = queue.Queue()
order_queue = queue.Queue()

threading.Thread(target=manage_couriers, args=(delivery_queue,) ).start()
threading.Thread(target=init_order_client).start()

kitchen = Kitchen(order_queue, delivery_queue)
app = Flask(__name__)


@app.route('/order',methods = ['POST'])
def post_order():
    try:
        json = request.get_json()
        order = Order.decode_json(json)
        kitchen.put_order(order)
    except InvalidOrderError as e:
        return "invalid order: {msg}".format(msg = e), 500
    except:
        return 'unknown error', 500
    return order.id, 200

@app.route('/order/<string:id>/status',methods = ['PUT'])
def update_order_status(id):
    try:
        json = request.get_json()
        status = OrderStatus.decode_json(json)
        kitchen.update_order_status(id, status)
    except InvalidOrderID as e:
        return "invalid order id: {}".format(e), 500
    except InvalidOrderStatus as e:
        return "invalid order status: {}".format(e), 500
    except:
        return 'unknown error', 500
    return '', 200

@app.route('/order/<string:id>/',methods = ['GET'])
def get_order(id):
    try:
        order = kitchen.get_order(id)
    except InvalidOrderID as e:
        return "invalid order id: {}".format(e), 500
    return json.dumps(order, indent=4, cls=OrderEncoder), 200

@app.route('/order',methods = ['GET'])
def get_orders():
    orders = kitchen.get_orders()
    return jsonify(
                    data=json.dumps(orders, indent=4),
                    status=200
                )

if __name__ == "__main__":
    app.run(debug=True)

# TODO: add logger for both debug and info
# TODO: response proper error json response
# TODO: in handlers, add exception for all handlers
# TODO: define consts for HTTP status codes