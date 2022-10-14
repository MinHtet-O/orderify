from shelf import *
from errors import *

SHELF_MANAGEMENT_TICK = 1

class ShelfManager:
    def __init__(self):
        self.__allowable_shelves:dict[ShelfTemp, Shelf] = {}
        self.__overflow_shelf: Shelf = None

    def add_allowable_shelf(self, cap: int, temp: ShelfTemp):
        if self.__shelf_exit(temp):
            raise ShelfAlreadyExits("{} shelf already exits".format(temp))
        self.__allowable_shelves[temp] = Shelf(cap, temp)

    def add_overflow_shelf(self, cap):
        if self.__overflow_shelf is not None:
            raise ShelfAlreadyExits("overflow shelf already exits")
        self.__overflow_shelf = Shelf(cap, None)

    def all_shelves_full(self) -> Boolean:
        return self.__overflow_shelf_full() and self.__allowable_shelves_full()

    def __allowable_shelves_full(self)-> Boolean:
        for key in self.__allowable_shelves:
            if not self.__allowable_shelves[key].check_full():
                return False
        return True

    def __overflow_shelf_full(self) -> Boolean:
        return self.__overflow_shelf.check_full()

    def peek_allowable_shelf(self, temp: ShelfTemp) -> List[Order]:
        if temp == None:
            return TempNotMatchErr("{} is not valid temperature").__format__(temp)
        if not self.__shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for temp {}".format(temp))
        return self.__allowable_shelves[temp].get_orders()

    def peek_overflow_shelf(self) -> List[Order]:
        return self.__overflow_shelf.get_orders()


    # TODO: change method name
    def __shelf_exit(self, temp) -> Boolean:
        if temp in self.__allowable_shelves:
            return True
        return False

    def put_order(self, order: Order):
        temp = order.temp

        if not self.__shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for this order temp {}".format(temp))

        if not self.__allowable_shelves[temp].check_full():
            self.__allowable_shelves[temp].put_order(order)
            return

        if not self.__overflow_shelf.check_full():
            self.__overflow_shelf.put_order(order)
            return

        raise NoEmptySpaceErr("no empty space in {} temp shelf".format(order.temp))

    def init_manager_thread(self, event):
        while True:
            event.wait()
            self.__update_deterioration()
            self.manage_shelves()
            event.clear()

    def manage_shelves(self):
        self.__discard_spoiled_orders()
        self.__order_replacement()

    def remove_order(self, order_id: string):
        orders = self.__order_iterator()
        for (index, order, shelf ) in orders:
            if order.id == order_id:
                print("ShelfManager: {} has is about to be removed from shelf".format(order.name))
                shelf.remove_order(index)
                return
        raise InvalidOrderID("order id {} not exists".format(id))


    # discard spoiled/ delivered orders
    def __discard_spoiled_orders(self):
        orders = self.__order_iterator()
        for (index, order, shelf ) in orders:
            if order.spoiled():
                print("ShelfManager: {} has spoiled and about to be removed from shelf".format(order.name))
                order.status = OrderStatus.FAILED
                shelf.remove_order(index)
                continue

        if self.all_shelves_full():
            self.__overflow_shelf.remove_random_order()

    def __order_replacement(self):
        if self.__overflow_shelf_full() and (not self.__allowable_shelves_full()):
                # move orders from overflow to allowable shelf
            for index, order in enumerate(self.__overflow_shelf.get_orders()):
                shelf = self.__allowable_shelves[order.temp]
                if shelf.check_full():
                    continue
                print("ShelfManager: {} with {} has moved to allowable shelf".format(order.name, order.temp))
                order = self.__overflow_shelf.remove_order(index)
                shelf.put_order(order)
                break

    def __update_deterioration(self):
        # update deterioration value for each shelf
        shelves = self.__shelf_iterator()
        for shelf in shelves:
            shelf.update_deterioration()

    # iterate all the orders within the shelves
    def __order_iterator(self):
        shelves = self.__shelf_iterator()
        for shelf in shelves:
            for index, order in enumerate(shelf.get_orders()):
                yield (index, order, shelf)

    # iterate all shelves
    def __shelf_iterator(self):
        for key in self.__allowable_shelves:
            yield self.__allowable_shelves[key]
        yield self.__overflow_shelf


class ShelfAlreadyExits(Exception):
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
