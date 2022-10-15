import queue
from pickup_area.pickup_area import PickupArea
from errors import InvalidOrderID, InvalidOrderError
from order.order import OrderStatus, Order


class Kitchen:
    def __init__(self, delivery_queue: queue.Queue, pickup_area: PickupArea):
        self.__orders: dict[str, Order] = {}
        self.__delivery_queue = delivery_queue
        self.__pickup_area = pickup_area

    def update_order_status(self, id: str, new_status: OrderStatus) -> None:
        if id not in self.__orders:
            raise InvalidOrderID("order id {} not exists".format(id))
        order = self.__orders[id]
        order.status = new_status
        if new_status == OrderStatus.DELIVERED:
            self.__pickup_area.remove_order(order.id)
        return

    def put_order(self, order: Order) -> None:

        if order.id in self.__orders:
            raise InvalidOrderError("Order id of {} already exits".format(order.id))
        self.__orders[order.id] = order

        exception = self.__pickup_area.put_order(order)
        if exception is not None:
            order.status = OrderStatus.FAILED
            raise exception
        self.__delivery_queue.put(order)
        order.status = OrderStatus.WAITING

    def get_order(self, order_id) -> Order:
        if order_id not in self.__orders.keys():
            raise InvalidOrderID("order id {} not exists".format(order_id))
        return self.__orders[order_id]
