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
    
    # Order is pending to be accepted
    PENDING = "PENDING"
    # Order is accepted from kitchen
    ACCEPTED = "ACCEPTED"
    # Order is ready and waiting for delivery
    WAITING = "WAITING"
    # Order has delivered
    DELIVERED = "DELIVERED"
    # Order has failed.
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
        self.update_status(OrderStatus.PENDING)
        self.inherent_value = None
        self.order_age = 0
    
    def check_spoiled(self) -> Boolean:
        return self.inherent_value < 0

    def check_delivered(self) -> Boolean:
        return self.status == OrderStatus.DELIVERED

    def update_status(self, order_status: OrderStatus):
        self.lock.acquire()
        self.status = order_status
        self.lock.release()

    def update_inherent_value(self, inherent_value):
        self.lock.acquire()
        self.inherent_value = inherent_value
        self.lock.release()

    def __repr__(self):
        str = """Order: {}
        name: {}
        temp: {}
        shelfLife: {}
        decayRate: {}""".format(
            self.id,
            self.name,
            self.temp,
            self.shelf_life,
            self.decay_rate
            )
        return str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    @staticmethod
    def decode_json(json):
        # TODO: validate each fields and return appropriate error
        # TODO: refactor as custom validator method
        
        if not 'id' in json:
            raise InvalidOrderError("id should not be empty")
        id = json["id"]
        name = json["name"]
        temp = json["temp"]
        shelf_life = json["shelfLife"]
        decay_rate = json["decayRate"],
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