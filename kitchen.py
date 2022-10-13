from shelf_manager import *
import queue

# the time it takes to prepare for each order
# the order is instantly cooked currently
PREP_TIME = 0


class Kitchen:
    def __init__(self, delivery_queue: queue.Queue, shelf_manager: ShelfManager):
        self.__orders: dict[str, Order] = {}
        self.__delivery_queue = delivery_queue
        self.__shelf_manager = shelf_manager

    def update_order_status(self, id: string, new_status: OrderStatus) -> None:
        if id not in self.__orders:
            raise InvalidOrderID("order id {} not exists".format(id))
        order = self.__orders[id]
        # TODO: refactor as new exeception
        if (order.status == OrderStatus.FAILED):
            raise InvalidOrderStatus("{} has already failed".format(order.name))
        if (order.status == OrderStatus.DELIVERED):
            raise InvalidOrderStatus("{} has already delivered".format(order.name))
        order.update_status(new_status)
        if new_status == OrderStatus.DELIVERED:
            self.__shelf_manager.remove_order(order.id)
        return

    def put_order(self, order: Order):
        if order.id in self.__orders:
            raise InvalidOrderError("Order id of {} already exits".format(order.id))
        self.__orders[order.id] = order
        self.__delivery_queue.put(order)
        self.__shelf_manager.put_order(order)
        order.update_status(OrderStatus.WAITING)

    def get_order(self, id):
        if id not in self.__orders.keys():
            raise InvalidOrderID("order id {} not exists".format(id))
        return self.__orders[id]

    #TODO: test properly
    def get_orders(self):
        return self.__orders

