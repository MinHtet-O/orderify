from http.client import ACCEPTED
import string
import threading

from enum import Enum
import json
from xmlrpc.client import Boolean

class ShelfTemp(str, Enum):
    HOT = "HOT"
    COLD = "COLD"
    FROZEN = "FROZEN"

    @staticmethod
    def decode_json(json):
        # TODO: validate each fields and return appropriate error
        # TODO: refactor as custom validator method
        if not 'temp' in json:
            raise InvalidOrderError("temp should not be empty")

        temp = json['temp'].upper()
        try:
            temp = OrderStatus[temp]
        except Exception as e:
            raise InvalidOrderError("{} is not valid temp".format(temp))
        return temp

class OrderStatus(str, Enum):

    PENDING = "PENDING" # Pending to be accepted from kitchen
    WAITING = "WAITING" # Ready/ Waiting for delivery
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

    @staticmethod
    def decode_json(json):
        # TODO: validate each fields and return appropriate error
        # TODO: refactor as custom validator method
        if not 'status' in json:
            raise InvalidOrderError("status should not be empty")
        # TODO: throw invalid status error
        status = json['status'].upper()
        try:
            status = OrderStatus[status]
        except Exception as e:
            raise InvalidOrderError("{} is not valid status".format(status))
        return status

class Order:
    def __init__(self,id: string, name: string, temp: ShelfTemp, shelfLife: int, decayRate: float):
        self.id = id
        self.name = name
        self.temp = temp
        self.shelf_life = shelfLife
        self.decay_rate = decayRate
        self.lock = threading.Lock()
        self.status = OrderStatus.PENDING
        self.order_age = 1
        self.inherent_value = 0
        self.valid_status_trans = {
            OrderStatus.PENDING: [OrderStatus.WAITING],
            OrderStatus.WAITING: [OrderStatus.DELIVERED, OrderStatus.FAILED]
        }

    # TODO: refactor to spoiled and delivered
    def check_spoiled(self) -> Boolean:
        return self.inherent_value < 0

    def check_delivered(self) -> Boolean:
        return self.status == OrderStatus.DELIVERED

    def __verify_status_trans(self, current: OrderStatus, next: OrderStatus) -> Boolean:
        valid_states = self.valid_status_trans[current]
        return next in valid_states

    def __verify_age_trans(self, current: int, new: int) -> Boolean:
        return new > current

    def update_status(self, new_status: OrderStatus):
        if not self.__verify_status_trans(self.status, new_status):
            raise InvalidOrderStatus("can not change order to {} which is already {}".format(new_status, self.status))
        self.lock.acquire()
        self.status = new_status
        self.lock.release()

    def update_age(self, new_order_age: int):
        if not self.__verify_age_trans(self.order_age, new_order_age):
            raise Exception("can not set order age smaller than current")
        self.lock.acquire()
        self.order_age = new_order_age
        self.lock.release()

    def update_inherent_value(self, inherent_value: float):
        self.lock.acquire()
        print("{} value is about to update to {}".format(self.name, inherent_value))
        self.inherent_value:float = inherent_value
        self.lock.release()

    def __repr__(self):
        str = "ID: {}, name: {}, temp: {}, value: {}".format(
            self.id,
            self.name,
            self.temp,
            self.inherent_value,
            )
        return str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    @staticmethod
    def decode_json(json):
        # TODO: validate each fields and return appropriate error
        # TODO: refactor as custom validator method
        temp = json["temp"].upper()
        if not 'id' in json:
            raise InvalidOrderError("id should not be empty")

        id = json["id"]
        name = json["name"]
        # TODO: error handling
        # convert string to enum
        temp: ShelfTemp = ShelfTemp[temp]
        shelf_life = json["shelfLife"]
        decay_rate = json["decayRate"]

        order = Order(id,name, temp, shelf_life, decay_rate)
        return order

class InvalidOrderError(Exception):
    pass
class InvalidOrderStatus(Exception):
    pass

class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
            data = dict()
            data['id'] = obj.id
            data['name'] = obj.name
            data['status'] = obj.status
            return data
