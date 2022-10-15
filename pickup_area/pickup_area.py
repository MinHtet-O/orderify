from shelf.shelf import Shelf
from shelf.temp_shelf import TempShelf
from order.order import Temp, Order
from errors import TempNotMatchErr, ShelfAlreadyExits, InvalidOrderID, NoEmptySpaceErr

class PickupArea:
    def __init__(self):
        self.__allowable_shelves:dict[Temp, Shelf] = {}
        self.__overflow_shelf: Shelf = None

    @property
    def allowable_shelves(self):
        return self.__allowable_shelves

    @property
    def overflow_shelf(self):
        return self.__overflow_shelf

    def get_allowable_shelf(self, temp:Temp) -> Shelf:
        if not self.__allowable_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for temp {}".format(temp))
        return self.__allowable_shelves[temp]

    # TODO: refactor  as shelf factory method
    def add_allowable_shelf(self, cap: int, temp: Temp) -> None:
        if self.__allowable_shelf_exit(temp):
            raise ShelfAlreadyExits("{} shelf already exits".format(temp))
        self.__allowable_shelves[temp] = TempShelf(cap, temp)

    def add_overflow_shelf(self, cap) -> None:
        if self.__overflow_shelf is not None:
            raise ShelfAlreadyExits("overflow shelf already exits")
        self.__overflow_shelf = Shelf(cap)

    def all_shelves_full(self) -> bool:
        return self.overflow_shelf_full() and self.allowable_shelves_full()

    def allowable_shelves_full(self)-> bool:
        for key in self.__allowable_shelves:
            if not self.__allowable_shelves[key].full():
                return False
        return True

    def overflow_shelf_full(self) -> bool:
        return self.__overflow_shelf.full()

    def __allowable_shelf_exit(self, temp) -> bool:
        if temp in self.__allowable_shelves:
            return True
        return False

    def remove_order(self, order_id: str) -> Order:
        orders = self.order_iterator()
        for (index, order, shelf ) in orders:
            if order.id == order_id:
                print("Pickup Area: {} has is about to be removed from shelf".format(order.name))
                return shelf.remove_order(index)
        raise InvalidOrderID("order id {} not exists".format(id))

    def put_order(self, order: Order) -> Exception:
        temp = order.temp

        if not self.__allowable_shelf_exit(temp):
            raise TempNotMatchErr("no shelf match for this order temp {}".format(temp))

        if not self.__allowable_shelves[temp].full():
            self.__allowable_shelves[temp].put_order(order)
            return

        if not self.__overflow_shelf.full():
            self.__overflow_shelf.put_order(order)
            return

        return NoEmptySpaceErr("no empty space for order {}".format(order.name))

    def order_iterator(self):
        shelves = self.shelf_iterator()
        for shelf in shelves:
            for index, order in enumerate(shelf.orders):
                yield (index, order, shelf)

    def shelf_iterator(self):
        for key in self.__allowable_shelves:
            yield self.__allowable_shelves[key]
        yield self.__overflow_shelf
