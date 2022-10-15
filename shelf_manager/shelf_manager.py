from pickup_area.pickup_area import PickupArea
import random
from order.order import Order, OrderStatus
from errors import ShelfManagerAssignedAlready
from typing import Optional

class ShelfManager:
    def __init__(self):
        self.__pickup_area: Optional[PickupArea] = None

    def assign(self, pickup_area: PickupArea) -> PickupArea:
        if self.__pickup_area is not None:
            raise ShelfManagerAssignedAlready("Unable to assign to more than one pickup area")
        self.__pickup_area = pickup_area
        return pickup_area

    def manage_shelves(self, event) -> None:
        while True:
            event.wait()
            self.__update_deterioration()
            self.__discard_spoiled_orders()
            self.__remove_order_on_full()
            self.__order_replacement()
            event.clear()

    def __remove_order_on_full(self) -> Order:
        if self.__pickup_area.all_shelves_full():
            shelf = self.__pickup_area.overflow_shelf
            # remove random order
            index = random.randint(0, shelf.size - 1)
            order = shelf.remove_order(index)
            order.status = OrderStatus.FAILED

    def __discard_spoiled_orders(self):
        orders = self.__pickup_area.order_iterator()
        for (index, order, shelf ) in orders:
            if order.spoiled():
                print("ShelfManager: {} has spoiled and about to be removed from shelf".format(order.name))
                order.status = OrderStatus.FAILED
                shelf.remove_order(index)
                continue

    def __order_replacement(self):
        pickup_area = self.__pickup_area
        if pickup_area.overflow_shelf_full() and (not pickup_area.allowable_shelves_full()):
            for index, order in enumerate(pickup_area.overflow_shelf.orders):
                allowable_shelf = pickup_area.get_allowable_shelf(order.temp)
                if not allowable_shelf.full():
                    print(f"ShelfManager: {order.name} with {order.temp} has replaced to allowable shelf")
                    order = pickup_area.overflow_shelf.remove_order(index)
                    allowable_shelf.put_order(order)
                    break

    def __update_deterioration(self):
        # update deterioration value for each shelf
        shelves = self.__pickup_area.shelf_iterator()
        for shelf in shelves:
            shelf.deteriorate_orders()
