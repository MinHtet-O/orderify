import threading
import queue
from order import *
from courior import *
from kitchen import *
from flask import Flask, jsonify, request

delivery_queue = queue.Queue()
order_queue = queue.Queue()

threading.Thread(target=courier, args=(delivery_queue,) ).start()
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
    # except:
    #     return '', 500
    return order.id, 200

@app.route('/order/<string:id>/',methods = ['GET'])
def get_order(id):
    order = kitchen.get_order(id)
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