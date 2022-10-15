import unittest,queue
from order.order import Order, Temp, OrderStatus
from shelf_manager.shelf_manager import ShelfManager
from kitchen.kitchen import Kitchen
from errors import InvalidOrderID, InvalidOrderError, InvalidOrderStatus
from pickup_area.pickup_area import  PickupArea

# TODO: define method to prepare test data

class KitchenTest(unittest.TestCase):
    def setUp(self):
        delivery_queue = queue.Queue()

        pickup_area = PickupArea()
        pickup_area.add_allowable_shelf(2, Temp.HOT)
        pickup_area.add_allowable_shelf(2, Temp.COLD)
        pickup_area.add_overflow_shelf(2)

        shelf_manager = ShelfManager()
        pickup_area = shelf_manager.assign(pickup_area)

        self.kitchen = Kitchen(delivery_queue, pickup_area)

    def test_placement(self):
        hot_order = Order("1","Hot Dog", Temp.HOT, 1, 1)
        cold_order = Order("2", "Ice Cream", Temp.COLD, 1, 1)
        self.kitchen.put_order(hot_order)
        self.kitchen.put_order(cold_order)

        # Expect: orders are placed in the order list
        self.assertEqual(self.kitchen.get_order(id = "1"), hot_order)
        self.assertEqual(self.kitchen.get_order(id = "2"), cold_order)

        # put another order with duplicate order id
        hot_order_duplicate = Order("1","Burger", Temp.HOT, 1, 1)
        # Expect: can not receive order with duplicate order id
        with self.assertRaises(InvalidOrderError):
            self.kitchen.put_order(hot_order_duplicate)

        # get order that doesn't exist
        with self.assertRaises(InvalidOrderID):
            self.kitchen.get_order("999")
        with self.assertRaises(InvalidOrderID):
            self.kitchen.get_order("-1")

    def test_update_order_status(self):
        hot_order = Order("1","Hot Dog", Temp.HOT, 1, 1)
        self.kitchen.put_order(hot_order)

        # Expect: the order status is waiting to deliver
        self.assertEqual(self.kitchen.get_order(id = "1").status, OrderStatus.WAITING)

        # update the order status
        self.kitchen.update_order_status("1", OrderStatus.DELIVERED)
        # Expect: the status becomes delivered
        self.assertEqual(self.kitchen.get_order(id = "1").status, OrderStatus.DELIVERED)


        # Expect: can not change the status of delivered/ failed order
        with self.assertRaises(InvalidOrderStatus):
            self.kitchen.update_order_status("1", OrderStatus.FAILED)

        # update the order status of order that doesn't exit
        with self.assertRaises(InvalidOrderID):
            self.kitchen.update_order_status("999", OrderStatus.DELIVERED)
        with self.assertRaises(InvalidOrderID):
            self.kitchen.update_order_status("-1", OrderStatus.DELIVERED)


