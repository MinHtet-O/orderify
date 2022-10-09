from http.client import ACCEPTED
import string
from unicodedata import name
from enum import Enum
import json

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
        try:
            status = OrderStatus[json['status'].upper()]
        except:
            raise InvalidOrderStatus("{} is not valid status".format(status))
        return status
        
    

class Order:
    # TODO: remove method
    def update_status(self, orderStatus: OrderStatus):
        self.status = orderStatus

    def __init__(self,id: string, name: string, temp: string, shelfLife: int, decayRate: float):
        self.id = id
        self.name = name
        self.temp = temp
        self.shelf_life = shelfLife
        self.decay_rate = decayRate
        self.update_status(OrderStatus.PENDING)

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