from config import ALLOWABLE_DECAY_MODS, OVERFLOW_DECAY_MODS, ORDER_AGE_INC
from errors import NoEmptySpaceErr, TempNotMatchErr
from order.order import *
from shelf.shelf import *
from shelf.calc_inherent import *
from order.temp import Temp
from typing import  Optional

class TempShelf(Shelf):
    def __init__(self, capacity: int, temp: Temp):
        self.__temp: Optional[Temp] = temp
        decay_mod:int = ALLOWABLE_DECAY_MODS[temp]
        super().__init__(capacity, decay_mod)

    @property
    def name(self):
        if self.__temp == None:
            return "overflow shelf"
        return "{} shelf".format(self.__temp)

    def put_order(self, order: Order):
        if self.__temp != order.temp:
                raise TempNotMatchErr("order temp {} can not put in shelf with temp {}".format(order.temp, self.__temp))
        super().put_order(order)



