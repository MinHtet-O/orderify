from lib2to3.pgen2.token import COLON
from sre_constants import ANY
import unittest
from shelf import *
from shelf_manager import *
import threading

# Define 3 allowable shelves with size of 1. and overflow shelves with size of 2
# put order with "HOT" temp
# put order with "FROZEN" temp
# put order with "COLD" temp
# expected: each order is in respective shelf

# class ShelfManagerTest(unittest.TestCase):
#     def setUp(self):
#         self.shelf_manager = ShelfManager()
#         self.shelf_manager.add_allowable_shelf(1, ShelfTemp.HOT)
#         self.shelf_manager.add_allowable_shelf(1, ShelfTemp.COLD)
#         self.shelf_manager.add_allowable_shelf(1, ShelfTemp.FROZEN)
#         self.shelf_manager.add_overflow_shelf(2)
#
#     def test_shelf_placement(self):
#         # Expect: unable to add more shelves
#         with self.assertRaises(ShelfAlreadyExits):
#             self.shelf_manager.add_allowable_shelf(1, ShelfTemp.HOT)
#         with self.assertRaises(ShelfAlreadyExits):
#             self.shelf_manager.add_allowable_shelf(1, ShelfTemp.FROZEN)
#         with self.assertRaises(ShelfAlreadyExits):
#             self.shelf_manager.add_overflow_shelf(2)
#
#     def test_order_placement(self):
#         hot_order1 = Order(id="1", name="Pizza", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         hot_order2 = Order(id="2", name="Hot Dog", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         hot_order3 = Order(id="3", name="Burger", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         cold_order1 = Order(id="4", name="Smoothie", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         cold_order2 = Order(id="5", name="Pepsi", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         frozen_order = Order(id="6", name="Ice Cream", temp=ShelfTemp.FROZEN, shelfLife=1, decayRate=1)
#
#         # Put three order
#         self.shelf_manager.put_order(hot_order1)
#         self.shelf_manager.put_order(cold_order1)
#         self.shelf_manager.put_order(frozen_order)
#
#         # Expect: each order are placed on the shelves with respective temperature
#         self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.HOT), [hot_order1])
#         self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.COLD), [cold_order1])
#         self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.FROZEN), [frozen_order])
#
#         # Put two more order
#         self.shelf_manager.put_order(hot_order2)
#         self.shelf_manager.put_order(hot_order3)
#
#         # Expect: additional orders are stored in the overflow shelf
#         self.assertEqual(self.shelf_manager.peek_orders(None), [hot_order2, hot_order3])
#
#         #Except: True, all shelves are full
#         self.assertEqual(self.shelf_manager.all_shelves_full(), True)
#
#         # Expect: unable to accept any order.
#         with self.assertRaises(NoEmptySpaceErr):
#             self.shelf_manager.put_order(cold_order2)
#
#     def test_remove_order_if_full(self):
#         hot_order1 = Order(id="1", name="Pizza", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         hot_order2 = Order(id="2", name="Hot Dog", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         cold_order1 = Order(id="3", name="Smoothie", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         cold_order2 = Order(id="4", name="Pepsi", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         frozen_order = Order(id="5", name="Ice Cream", temp=ShelfTemp.FROZEN, shelfLife=1, decayRate=1)
#
#         # put 1 order in each allowable shelves
#         self.shelf_manager.put_order(hot_order1)
#         self.shelf_manager.put_order(cold_order1)
#         self.shelf_manager.put_order(frozen_order)
#         # put 2 orders in overflow shelves
#         self.shelf_manager.put_order(hot_order2)
#         self.shelf_manager.put_order(cold_order2)
#         # manage shelves
#         self.shelf_manager.manage_shelves()
#
#         # Expect: random order has dropped from overflow shelves
#         # Expect: now overflow shelf has only one order
#         self.assertEqual(len(self.shelf_manager.peek_orders(None)), 1)
#
#     def test_order_replacement(self):
#         hot_order1 = Order(id="1", name="Pizza", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         hot_order2 = Order(id="2", name="Hot Dog", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
#         cold_order1 = Order(id="4", name="Smoothie", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         cold_order2 = Order(id="4", name="Pepsi", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
#         frozen_order = Order(id="6", name="Ice Cream", temp=ShelfTemp.FROZEN, shelfLife=1, decayRate=1)
#
#         # put 1 order in each allowable shelves
#         self.shelf_manager.put_order(hot_order1)
#         self.shelf_manager.put_order(cold_order1)
#         self.shelf_manager.put_order(frozen_order)
#         # put 2 orders in overflow shelves
#         self.shelf_manager.put_order(hot_order2)
#         self.shelf_manager.put_order(cold_order2)
#         # hot order has spoiled
#         hot_order1.update_inherent_value(-0.5)
#         # cold order has delivered
#         cold_order1.update_status(OrderStatus.DELIVERED)
#         # manage shelves
#         self.shelf_manager.manage_shelves()
#
#         # Expect: spoiled hot_order1 has removed from the shelf
#         self.assertEqual(hot_order1 not in self.shelf_manager.peek_orders(ShelfTemp.HOT), True)
#         # Expect: spoiled hot_order1 status becomes FAILED
#         self.assertEqual(hot_order1.status, OrderStatus.FAILED)
#         # Expect: delivered cold_order1 has removed from the shelf
#         self.assertEqual(cold_order1 not in self.shelf_manager.peek_orders(ShelfTemp.COLD), True)
#         # Expect: frozen_order is still in the shelf
#         self.assertEqual(frozen_order in self.shelf_manager.peek_orders(ShelfTemp.FROZEN), True)
#         # Expect: The overflow shelf is full, hot_order2 is moved to allowable shelf
#         self.assertEqual(hot_order2 in self.shelf_manager.peek_orders(ShelfTemp.HOT), True)


class UpdateDeteriorationTest(unittest.TestCase):
    def test_deterioration_overtime(self):
        shelf_manager = ShelfManager(0.5)
        shelf_manager.add_allowable_shelf(1, ShelfTemp.HOT)
        shelf_manager.add_overflow_shelf(2)

        # create two order with same shelf life and decay rate
        hot_order1 = Order(id="1", name="Pizza", temp=ShelfTemp.HOT, shelfLife=300, decayRate=0.45)
        hot_order2 = Order(id="2", name="Noodle", temp=ShelfTemp.HOT, shelfLife=300, decayRate=0.45)

        # put first order in the allowable shelf
        shelf_manager.put_order(hot_order1)
        # put second order in the overflow shelf
        # shelf_manager.put_order(hot_order2)

        # initiate the thread for shelf_manager
        # shelf_manager.init_manager_thread()
        print(shelf_manager.peek_orders(ShelfTemp.HOT)[0])
        print(shelf_manager.peek_orders(ShelfTemp.HOT)[0])
        threading.Thread(target=shelf_manager.init_manager_thread).start()

        while True:
            print(shelf_manager.peek_orders(ShelfTemp.HOT)[0].inherent_value)

unittest.main()

# test: not accept temp of any in allowable shelf
# test: remove order
