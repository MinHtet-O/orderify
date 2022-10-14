import unittest
from kitchen import *

# TODO: define method to prepare test data
from order.order_status import OrderStatus
from order.temp import Temp


class KitchenTest(unittest.TestCase):
    def setUp(self):
        delivery_queue = queue.Queue()
        shelf_manager = ShelfManager()
        shelf_manager.add_allowable_shelf(2, Temp.HOT)
        shelf_manager.add_allowable_shelf(2, Temp.COLD)
        shelf_manager.add_overflow_shelf(2)
        self.kitchen = Kitchen(delivery_queue, shelf_manager)

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

unittest.main()

# test: update order status to delivered, the order should be remove be removed

