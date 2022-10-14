from http.client import ACCEPTED
import string
import threading

from enum import Enum
import json
from xmlrpc.client import Boolean

def lock_attr(func):
    def wrapper(*args, **kwargs):
        with args[0].lock:
            return func(*args, **kwargs)
    return wrapper

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
        self.__id = id
        self.__name = name
        self.__temp = temp
        self.__shelf_life = shelfLife
        self.__decay_rate = decayRate
        self.__status = OrderStatus.PENDING
        self.__order_age = 0
        self.__inherent_value = 1
        self.__status_trans = {
            OrderStatus.PENDING: [OrderStatus.WAITING, OrderStatus.FAILED],
            OrderStatus.WAITING: [OrderStatus.DELIVERED, OrderStatus.FAILED]
        }
        self.lock = threading.Lock()

    # TODO: refactor to spoiled and delivered
    def spoiled(self) -> Boolean:
        return self.inherent_value < 0

    def delivered(self) -> Boolean:
        return self.status == OrderStatus.DELIVERED

    def __verify_status_trans(self, current: OrderStatus, next: OrderStatus) -> Boolean:
        valid_states = self.__status_trans[current]
        return next in valid_states

    def __verify_age_trans(self, current: int, new: int) -> Boolean:
        return new > current

    def __verify_inherent_value_trans(self, current: int, new: int) -> Boolean:
        return new < current

    def __repr__(self):
        str = "ID: {}, name: {}, temp: {}, value: {}, order_age {}".format(
            self.__id,
            self.__name,
            self.__temp,
            self.__inherent_value,
            self.__order_age
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

    @property
    @lock_attr
    def id(self):
        return self.__id

    @id.setter
    @lock_attr
    def id(self, id):
        self.__id = id

    @property
    @lock_attr
    def name(self):
        return self.__name

    @name.setter
    @lock_attr
    def name(self, name):
        self.__name = name

    @property
    @lock_attr
    def temp(self):
        print("inside temp getter")
        print(self.__temp)
        return self.__temp

    @temp.setter
    @lock_attr
    def temp(self, temp):
        self.__temp = temp

    @property
    @lock_attr
    def shelf_life(self):
        return self.__shelf_life

    @shelf_life.setter
    @lock_attr
    def shelf_life(self, shelf_life):
        self.__shelf_life = shelf_life

    @property
    @lock_attr
    def decay_rate(self):
        return self.__decay_rate

    @decay_rate.setter
    @lock_attr
    def decay_rate(self, decay_rate):
        self.__decay_rate = decay_rate

    @property
    @lock_attr
    def status(self):
        return self.__status

    @status.setter
    @lock_attr
    def status(self, status):
        print("inside status setter")
        if not self.__verify_status_trans(current= self.__status,next= status):
            raise InvalidOrderStatus("can not change order to {} which is already {}".format(status, self.__status))
        self.__status = status

    @property
    @lock_attr
    def order_age(self):
        return self.__order_age

    @order_age.setter
    @lock_attr
    def order_age(self, order_age):
        if not self.__verify_age_trans(current= self.__order_age, new = order_age):
            raise Exception("can not set order age smaller than current")
        self.__order_age = order_age

    @property
    @lock_attr
    def inherent_value(self):
        return self.__inherent_value

    @inherent_value.setter
    @lock_attr
    def inherent_value(self, inherent_value):
        if not self.__verify_inherent_value_trans(current= self.__inherent_value, new = inherent_value):
            raise Exception("can not set inherent bigger than current")
        print("{} value is about to update to {}".format(self.__name, inherent_value))
        self.__inherent_value = inherent_value

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
