from order.order import OrderStatus
from pickup_area.pickup_area import PickupArea
from shelf_policy.shelf_policy_interface import ShelfPolicy

# update deterioration for each order
class OrderDeteriorator(ShelfPolicy):
    def apply_policy(self, pickup_area: PickupArea):
        orders = pickup_area.order_iterator()
        for (index, order, shelf) in orders:
            order.inc_order_age()
            value = self.calc_inherent_value(
                shelf_life=order.shelf_life,
                order_age=order.order_age,
                decay_rate=order.decay_rate,
                decay_mod=shelf.decay_mod
            )
            print(f"ShelfPolicy: {order.name} value about to become {order.inherent_value}")
            order.inherent_value = value

    def calc_inherent_value(self, shelf_life, order_age, decay_rate, decay_mod) -> float:
        value = (shelf_life - order_age - decay_rate * (order_age * decay_mod)) / shelf_life
        value = (round(value, 8))
        return value
