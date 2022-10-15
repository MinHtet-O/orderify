from errors import NoEmptySpaceErr
from order.order import Order
from config import OVERFLOW_DECAY_MODS
from shelf.calc_inherent import *

class Shelf:
    def __init__(self, capacity: int, decay_mod: int = OVERFLOW_DECAY_MODS):
        self.__store: list[Order] = []
        self.__capacity = capacity
        self.__decay_mod = decay_mod

    @property
    def name(self):
        return "default shelf"
    @property
    def orders(self):
        return self.__store
    @property
    def size(self):
        return len(self.__store)
    @property
    def temp(self):
        return self.__temp

    def full(self) -> bool:
        return len(self.__store) >= self.__capacity

    def put_order(self, order: Order) -> None:
        if self.full():
            raise NoEmptySpaceErr("shelf has reached to it's max storage of {}".format(self.__capacity))
        print("Shelf: {} has successfully placed in {}".format(order.name, self.name))
        self.__store.append(order)

    def deteriorate_orders(self) -> None:
        for order in self.__store:
            order.inc_order_age()
            value = calc_inherent_value(
                shelf_life=order.shelf_life,
                order_age= order.order_age,
                decay_rate= order.decay_rate,
                decay_mod=self.__decay_mod
            )
            order.inherent_value = value

    def remove_order(self, index: int)->Order:
        print("Shelf: {} is removed from {}".format(self.__store[index].name, self.name))
        return self.__store.pop(index)
