from time import sleep, time
from shelf import *
import threading

# TODO: add status field to Order

# every SHELF_MANAGEMENT_INTERVAL sec, shelf manager will
# 1. update detoration values for the orders
# 2. discard orders with value less than 0
# 3. discard orders with status delivered
# 4. if overflow shelf is full, existing order should moved to allowable shelf
# 5. if all full, random order from overflow shelf is discarded
SHELF_MANAGEMENT_INTERVAL = 1

# every DETORATION_TIMER sec, shelf_life of each order will increase by SHELF_LIFE_INC
SHELF_LIFE_INC = 10

class ShelfManager:
    def __init__(self, allowable_shelves: list[Shelf], overflow_shelf: Shelf):
        self.allowable_shelves = dict()
        self.overflow_shelf = overflow_shelf
        threading.Thread(target=self.__update_order_age).start()

    def check_shelves_full(self):
        for shelf_key in self.allowable_shelves:
            if not self.allowable_shelves[shelf_key].check_full():
                return False
        return self.overflow_shelf.check_full()
        

    def put_order(self, order: Order):
        temp = order.temp
        
        if temp not in self.allowable_shelves:
            raise TempNotMatchErr("no shelf match for temp {}".format(temp))
        
        if not self.allowable_shelves[temp].check_full():
            self.allowable_shelves[temp].put_order(order)
            return

        if not self.overflow_shelf.check_full():
            self.overflow_shelf.put_order(order)
            return

        raise NoEmptySpaceErr("all shelves are full")

    def __update_order_age(self):
        # initialize the thread to update order age every x second
        while True:
            time.sleep(SHELF_MANAGEMENT_INTERVAL)
            self.update_deterioration()
            # TODO: discard orders less than 0
            # TODO: discard orders with delivered status
            # TODO: order moved to allowable shelf if overflow is full
            # TODO: ramdom order from overflow is dropped if all shelves are full
        

    def remove_order(self):
        pass

    def update_deterioration(self):
        #list through items and update deterioration value
        for shelf_key in self.allowable_shelves:
            self.allowable_shelves[shelf_key].update_deterioration()
        self.overflow_shelf.update_deterioration()

    def remove_delivererd_order(self):
        #list through items and remove delivered order
        pass

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

