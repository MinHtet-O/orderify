import threading
import queue
from flask import Flask, jsonify, request

delivery_queue = queue.Queue()

# def courier():
#     while True:
#         item = delivery_queue.get()
#         if item == None:
#             print("All items delivered")
#             break
#         print(f'Delivering on {item}')


# threading.Thread(target=courier).start()


app = Flask(__name__)

@app.route('/order',methods = ['POST'])
def post_order():
    test = request.get_json()
    print(test)
    return 'This route is not available yet', 404

@app.route('/order/<string:id>/',methods = ['GET'])
def get_order(id):
    return 'This route is not available yet', 404
      

if __name__ == "__main__":
    app.run(debug=True)