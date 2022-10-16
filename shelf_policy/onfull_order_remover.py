import random
from pickup_area.pickup_area import PickupArea
from order.order import Order, OrderStatus
from shelf_policy.shelf_policy_interface import ShelfPolicy
import random

# remove order if all shelves are full
class OnFullOrderRemover(ShelfPolicy):
    def apply_policy(self, pickup_area: PickupArea):
        if pickup_area.all_shelves_full():
            shelf = pickup_area.overflow_shelf
            # remove random order
            index = random.randint(0, shelf.size - 1)
            order = shelf.remove_order(index)
            order.status = OrderStatus.FAILED
            return order