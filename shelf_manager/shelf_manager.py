from shelf.shelf import *
from errors import *

class ShelfManager:
    def __init__(self):
        self.__allowable_shelves:dict[Temp, Shelf] = {}
        self.__overflow_shelf: Shelf = None

    # TODO: refactor into shelf factory method
    def add_allowable_shelf(self, cap: int, temp: Temp):
        if self.__allowable_shelf_exit(temp):
            raise ShelfAlreadyExits("{} shelf already exits".format(temp))
        self.__allowable_shelves[temp] = Shelf(cap, temp)

    def add_overflow_shelf(self, cap):
        if self.__overflow_shelf is not None:
            raise ShelfAlreadyExits("overflow shelf already exits")
        self.__overflow_shelf = Shelf(cap, None)

    def all_shelves_full(self) -> bool:
        return self.__overflow_shelf_full() and self.__allowable_shelves_full()

    def __allowable_shelves_full(self)-> bool:
        for key in self.__allowable_shelves:
            if not self.__allowable_shelves[key].check_full():
                return False
        return True

    def __overflow_shelf_full(self) -> bool:
        return self.__overflow_shelf.check_full()

    def peek_allowable_shelf(self, temp: Temp) -> List[Order]:
        if temp == None:
            return TempNotMatchErr("{} is not valid temperature").__format__(temp)
        if not self.__allowable_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for temp {}".format(temp))
        return self.__allowable_shelves[temp].get_orders()

    def peek_overflow_shelf(self) -> List[Order]:
        return self.__overflow_shelf.get_orders()

    def __allowable_shelf_exit(self, temp) -> bool:
        if temp in self.__allowable_shelves:
            return True
        return False

    def put_order(self, order: Order) -> Exception:
        temp = order.temp

        if not self.__allowable_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for this order temp {}".format(temp))

        if not self.__allowable_shelves[temp].check_full():
            self.__allowable_shelves[temp].put_order(order)
            return

        if not self.__overflow_shelf.check_full():
            self.__overflow_shelf.put_order(order)
            return

        return NoEmptySpaceErr("no empty space for order {}".format(order.name))

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
