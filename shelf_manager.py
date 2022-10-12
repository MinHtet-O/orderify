from ast import Or
from operator import index
from time import time
from typing import Generator, List
from xmlrpc.client import Boolean
from shelf import *


SHELF_TICK_INTERVAL = 1

class ShelfManager:
    def __init__(self, allowable_shelves: dict[ShelfTemp, Shelf], overflow_shelf: Shelf):
        self.allowable_shelves = allowable_shelves
        self.overflow_shelf = overflow_shelf
        
    def allowable_shelves_full(self)-> Boolean:
        for key in self.allowable_shelves:
            if not self.allowable_shelves[key].check_full():
                return False
        return True

    def overflow_shelf_full(self) -> Boolean:
        return self.overflow_shelf.check_full()

    def all_shelves_full(self) -> Boolean:
        return self.overflow_shelf_full() and self.allowable_shelves_full()
        
    def peek_orders(self, temp: ShelfTemp) -> List[Order]:
        if temp == None:
            return self.overflow_shelf.get_orders()

        if not self.temp_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for temp {}".format(temp))
        return self.allowable_shelves[temp].get_orders()
        
    # TODO: change method name
    def temp_shelf_exit(self, temp) -> Boolean:
        if temp in self.allowable_shelves:
            return True
        return False
        
    def put_order(self, order: Order):
        temp = order.temp
        
        if not self.temp_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for this order temp {}".format(temp))
        
        if not self.allowable_shelves[temp].check_full():
            self.allowable_shelves[temp].put_order(order)
            return

        if not self.overflow_shelf.check_full():
            self.overflow_shelf.put_order(order)
            return

        raise NoEmptySpaceErr("all shelves are full")

    # TODO: init function from the outside caller
    def init_manager_thread(self):
        while True:
            time.sleep(SHELF_TICK_INTERVAL)
            self.manage_shelves()
            self.update_deterioration()
                   
    def manage_shelves(self):
        orders = self.order_iterator()
        for (index, order, shelf ) in orders:
            if order.check_spoiled() or order.check_delivered():
                shelf.remove_order(index)
                continue

        if self.overflow_shelf_full():
            if self.allowable_shelves_full():
                self.overflow_shelf.remove_random_order()
            else:
                # move order from overflow to allowable shelf
                for index, order in enumerate(self.overflow_shelf.get_orders()):
                    shelf =  self.allowable_shelves[order.temp]
                    if shelf.check_full():
                        continue
                    order = self.overflow_shelf.remove_order(index)
                    shelf.put_order(order)
                    break


    def update_deterioration(self):
        # update deterioration value for each shelf
        shelves = self.shelf_iterator()
        for shelf in shelves:
            shelf.update_deterioration()

    # iterate all the orders within the shelves
    def order_iterator(self) -> Generator[int, Order, Shelf]:
        shelves = self.shelf_iterator()
        for shelf in shelves(self):
            for index, order in enumerate(shelf.get_orders()):
                yield (index, order, shelf)

    # iterate all shelves
    def shelf_iterator(self) -> Generator[Shelf]:
        for key in self.allowable_shelves:
            yield self.allowable_shelves[key]
        yield self.overflow_shelf
            



# Define 3 allowable shelves with size of 1. and overflow shelves with size of 2
# put order with "HOT" temp
# put order with "FROZEN" temp
# put order with "COLD" temp
# expected: each order is in respective shelf

# put 2 more order with "HOT" temp
# expected : they are placed in the allowable shelf
# expected : all shelves are full

# put 1 more order with "HOT" temp
# expected : raise no empty space exception

# update 1 order value to -1
# update 1 order status to delivered

# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : orders with status delivered (or) value less than 0 are removed

# put 1 order in HOT, 1 order in FROZEN, 2 order in overflow shelves
# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : 1 COLD item from overflow shelves is put back to COLD allowable shelves

# put 1 order in HOT, 1 order in FROZEN,1 order in COLD and 2 order in overflow shelves
# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : random item from overflow sheles is dropped