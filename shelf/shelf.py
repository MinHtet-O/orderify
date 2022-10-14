from typing import List

from config import ALLOWABLE_DECAY_MODS, OVERFLOW_DECAY_MODS, ORDER_AGE_INC
from errors import NoEmptySpaceErr, TempNotMatchErr
from order.order import *
import random
from shelf.calc_inherent import *
from order.temp import Temp

class Shelf:
    def __init__(self, capacity: int, temp: Temp):
        self.store: list[Order] = []
        self.capacity = capacity
        self.temp = temp
        if temp == None:
            self.decay_mod: int = OVERFLOW_DECAY_MODS
        else:
            self.decay_mod:int = ALLOWABLE_DECAY_MODS[temp]
    @property
    def name(self):
        if self.temp == None:
            return "overflow shelf"
        return "{} shelf".format(self.temp)

    def get_orders(self) -> List[Order]:
        return self.store

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
        print("Shelf: {} has successfully placed in {}".format(order.name, self.name))
        self.store.append(order)

    def update_deterioration(self):
        for order in self.store:
            order.order_age = order.order_age + ORDER_AGE_INC
            value = calc_inherent_value(
                shelf_life=order.shelf_life,
                order_age= order.order_age,
                decay_rate= order.decay_rate,
                decay_mod=self.decay_mod
            )
            order.inherent_value = value

    def remove_order(self, index: int)->Order:
        print("{} Shelf: {} is removed".format(self.temp, self.store[index].name))
        return self.store.pop(index)

    def remove_random_order(self) -> Order:
        order_index = random.randint(0, len(self.store)-1)

        return self.remove_order(order_index)



