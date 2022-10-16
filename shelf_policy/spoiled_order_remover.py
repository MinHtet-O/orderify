from order.order import OrderStatus
from pickup_area.pickup_area import PickupArea
from shelf_policy.shelf_policy_interface import ShelfPolicy

class SpoiledOrderRemover(ShelfPolicy):
    # SpoiledOrderRemover
    def apply_policy(self, pickup_area: PickupArea):
        orders = pickup_area.order_iterator()
        for (index, order, shelf) in orders:
            if order.spoiled():
                print("ShelfPolicy: {} has spoiled and about to be removed from shelf".format(order.name))
                order.status = OrderStatus.FAILED
                shelf.remove_order(index)
                continue
