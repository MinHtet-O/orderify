from typing import List
from order import *
import random

ALLOWABLE_DECAY_MODS = {
    ShelfTemp.HOT: 1,
    ShelfTemp.COLD: 1,
    ShelfTemp.FROZEN: 1,
    
}
OVERFLOW_DECAY_MODS = 2

# shelf_life of each order will increase by SHELF_LIFE_INC continuously
SHELF_LIFE_INC = 10

class Shelf:
    def __init__(self, capacity: int, temp: ShelfTemp ):
        self.store: list[Order] = []
        self.capacity = capacity
        self.temp = temp
        if temp == None:
            self.decay_mod: int = OVERFLOW_DECAY_MODS
        else:
            self.decay_mod:int = ALLOWABLE_DECAY_MODS[temp]

    def get_orders(self) -> List[Order]:
        return self.store

    def occupied_storage(self) -> int:
        return len(self.store)

    def check_full(self):
        if len(self.store) >= self.capacity:
            return True
        return False

    def put_order(self, order: Order):
        if self.temp != None:
            if self.temp != order.temp: 
                raise TempNotMatchErr("order temp {} can not put in shelf with temp {}".format(order.temp, self.temp))
        if self.check_full():
            raise NoEmptySpaceErr("shelf has reached to it's max storage of {}".format(self.capacity))
        self.store.append(order)
        
    def update_deterioration(self):
        for order in self.store:
            # TODO: decide plus or multiply
            new_shelf_life = order.shelf_life + SHELF_LIFE_INC
            value = calc_inherent_value(
                shelf_life=new_shelf_life,
                order_age= order.order_age,
                decay_rate= order.decay_rate,
                decay_mod=self.decay_mod
            )
            order.update_inherent_value(value)

    def remove_order(self, index: int)->Order:
        return self.store.pop(index)

    def remove_random_order(self) -> Order:
        order_index = random.randint(0, len(self.store)-1)
        return self.remove_order(order_index) 

def calc_inherent_value(shelf_life, order_age, decay_rate,decay_mod):
    value = (shelf_life - order_age - decay_rate* (order_age*decay_mod))/ shelf_life
    value = (round(value,8))
    return value

class NoEmptySpaceErr(Exception):
    pass

class TempNotMatchErr(Exception):
    pass

# TODO: factory method for shelf

# Test: get orders