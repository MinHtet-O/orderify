from order.order import OrderStatus
from pickup_area.pickup_area import PickupArea
from shelf_policy.shelf_policy_interface import ShelfPolicy

# move order from overflow shelf to allowable shelf
class OrderRelocator(ShelfPolicy):
    def apply_policy(self, pickup_area: PickupArea):
        pickup_area = pickup_area
        if pickup_area.overflow_shelf_full() and (not pickup_area.allowable_shelves_full()):
            for index, order in enumerate(pickup_area.overflow_shelf.orders):
                allowable_shelf = pickup_area.get_allowable_shelf(order.temp)
                if not allowable_shelf.full():
                    print(f"ShelfPolicy: {order.name} with {order.temp} has replaced to allowable shelf")
                    order = pickup_area.overflow_shelf.remove_order(index)
                    allowable_shelf.put_order(order)
                    break
