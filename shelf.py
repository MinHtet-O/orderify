from typing import Any
from unicodedata import name
from enum import Enum

# TODO: add status field to Order
class ShelfTemp(str, Enum):
    HOT = "PENDING"
    COLD = "ACCEPTED"
    FROZEN = "WAITING"
    ANY = "DELIVERED"

DECAY_MODS = {
    ShelfTemp.HOT: 1,
    ShelfTemp.COLD: 1,
    ShelfTemp.FROZEN: 1,
    ShelfTemp.ANY: 2
}

class Shelf:
    def __init__(self, size: int, temp: ShelfTemp, decay_mod ):
        self.store = []
        self.size = size
        self.temp = temp
        self.decay_mod = decay_mod
        pass

    def check_full(self):
        pass

    def put_order(self):
        pass

    def remove_order(self):
        pass

    def update_deteriorate(self):
        #list through items and update deterioration value
        pass
    
def get_inherent_value(shelf_life, order_age, decay_rate,decay_mod):
    value = (shelf_life - order_age - decay_rate* (order_age*decay_mod))/ shelf_life
    value = (round(value,8))
    return value
