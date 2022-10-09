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
    

class Order:
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
        str = """Order: {id}
        name: {name}
        temp: {temp}
        shelfLife: {shelfLife}
        decayRate: {decayRate}""".format(
            id = self.id,
            name = self.name,
            temp = self.temp,
            shelfLife = self.shelf_life,
            decayRate = self.decay_rate
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
    
class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
            data = dict()
            data['id'] = obj.id
            data['name'] = obj.name
            data['status'] = obj.status
            return data