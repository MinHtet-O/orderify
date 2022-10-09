import threading
import queue
from model.order import *
from courior import *
from flask import Flask, jsonify, request

delivery_queue = queue.Queue()
threading.Thread(target=courier, args=(delivery_queue,) ).start()

app = Flask(__name__)
@app.route('/order',methods = ['POST'])
def post_order():
    try:
        json = request.get_json()
        order = Order.decodeFromJSON(json)
        delivery_queue.put(order)
    except InvalidOrderError as e:
        # TODO: response proper error json response
        return "invlaid order: {msg}".format(msg = e), 500
    except:
        return '', 500
    return order.id, 200

@app.route('/order/<string:id>/',methods = ['GET'])
def get_order(id):
    return 'This route is not available yet', 404
      
if __name__ == "__main__":
    app.run(debug=True)


# TODO: add logger for both debug and info