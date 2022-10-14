import time
import unittest
from shelf_manager import *
import threading

class ShelfManagerTest(unittest.TestCase):
    def setUp(self):
        self.shelf_manager = ShelfManager()
        self.shelf_manager.add_allowable_shelf(1, Temp.HOT)
        self.shelf_manager.add_allowable_shelf(1, Temp.COLD)
        self.shelf_manager.add_allowable_shelf(1, Temp.FROZEN)
        self.shelf_manager.add_overflow_shelf(2)

    def test_shelf_placement(self):
        # Expect: unable to add more shelves
        with self.assertRaises(ShelfAlreadyExits):
            self.shelf_manager.add_allowable_shelf(1, Temp.HOT)
        with self.assertRaises(ShelfAlreadyExits):
            self.shelf_manager.add_allowable_shelf(1, Temp.FROZEN)
        with self.assertRaises(ShelfAlreadyExits):
            self.shelf_manager.add_overflow_shelf(2)

    def test_order_placement(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=1, decayRate=1)
        hot_order3 = Order(id="3", name="Burger", temp=Temp.HOT, shelfLife=1, decayRate=1)
        cold_order1 = Order(id="4", name="Smoothie", temp=Temp.COLD, shelfLife=1, decayRate=1)
        cold_order2 = Order(id="5", name="Pepsi", temp=Temp.COLD, shelfLife=1, decayRate=1)
        frozen_order = Order(id="6", name="Ice Cream", temp=Temp.FROZEN, shelfLife=1, decayRate=1)

        # Put three order
        self.shelf_manager.put_order(hot_order1)
        self.shelf_manager.put_order(cold_order1)
        self.shelf_manager.put_order(frozen_order)

        # Expect: each order are placed on the shelves with respective temperature
        self.assertEqual(self.shelf_manager.peek_allowable_shelf(Temp.HOT), [hot_order1])
        self.assertEqual(self.shelf_manager.peek_allowable_shelf(Temp.COLD), [cold_order1])
        self.assertEqual(self.shelf_manager.peek_allowable_shelf(Temp.FROZEN), [frozen_order])

        # Put two more order
        self.shelf_manager.put_order(hot_order2)
        self.shelf_manager.put_order(hot_order3)

        # Expect: additional orders are stored in the overflow shelf
        self.assertEqual(self.shelf_manager.peek_overflow_shelf(), [hot_order2, hot_order3])

        #Except: True, all shelves are full
        self.assertEqual(self.shelf_manager.all_shelves_full(), True)

        # Expect: unable to accept any order.
        with self.assertRaises(NoEmptySpaceErr):
            self.shelf_manager.put_order(cold_order2)

    def test_remove_order(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        self.shelf_manager.put_order(hot_order1)
        self.shelf_manager.remove_order("1")

        # Expect: order with id 1 is removed from HOT shelf
        self.assertEqual(hot_order1 not in self.shelf_manager.peek_allowable_shelf(Temp.HOT), True)

        # Expect: unable to remove order that doesn't exit
        with self.assertRaises(InvalidOrderID):
          self.shelf_manager.remove_order("999")


    def test_remove_order_if_full(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=1, decayRate=1)
        cold_order1 = Order(id="3", name="Smoothie", temp=Temp.COLD, shelfLife=1, decayRate=1)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelfLife=1, decayRate=1)
        frozen_order = Order(id="5", name="Ice Cream", temp=Temp.FROZEN, shelfLife=1, decayRate=1)

        # put 1 order in each allowable shelves
        self.shelf_manager.put_order(hot_order1)
        self.shelf_manager.put_order(cold_order1)
        self.shelf_manager.put_order(frozen_order)
        # put 2 orders in overflow shelves
        self.shelf_manager.put_order(hot_order2)
        self.shelf_manager.put_order(cold_order2)
        # manage shelves
        self.shelf_manager.manage_shelves()

        # Expect: random order has dropped from overflow shelves
        # Expect: now overflow shelf has only one order
        self.assertEqual(len(self.shelf_manager.peek_overflow_shelf()), 1)

    def test_order_replacement(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=1, decayRate=1)
        cold_order1 = Order(id="4", name="Smoothie", temp=Temp.COLD, shelfLife=1, decayRate=1)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelfLife=1, decayRate=1)
        frozen_order = Order(id="6", name="Ice Cream", temp=Temp.FROZEN, shelfLife=1, decayRate=1)

        # put 1 order in each allowable shelves
        self.shelf_manager.put_order(hot_order1)
        self.shelf_manager.put_order(cold_order1)
        self.shelf_manager.put_order(frozen_order)
        # put 2 orders in overflow shelves
        self.shelf_manager.put_order(hot_order2)
        self.shelf_manager.put_order(cold_order2)
        # hot order has spoiled
        hot_order1.inherent_value = -0.5

        # # manage shelves
        self.shelf_manager.manage_shelves()

        # Expect: spoiled hot_order1 has removed from the shelf
        self.assertEqual(hot_order1 not in self.shelf_manager.peek_allowable_shelf(Temp.HOT), True)
        # Expect: spoiled hot_order1 status becomes FAILED
        self.assertEqual(hot_order1.status, OrderStatus.FAILED)
        # Expect: delivered cold_order1 has removed from the shelf

        # Expect: frozen_order is still in the shelf
        self.assertEqual(frozen_order in self.shelf_manager.peek_allowable_shelf(Temp.FROZEN), True)
        # Expect: The overflow shelf is full, hot_order2 is moved to allowable shelf
        self.assertEqual(hot_order2 in self.shelf_manager.peek_allowable_shelf(Temp.HOT), True)

class UpdateDeteriorationTest(unittest.TestCase):
    def test_deterioration_overtime(self):
        shelf_manager = ShelfManager()
        shelf_manager.add_allowable_shelf(1, Temp.HOT)
        shelf_manager.add_overflow_shelf(2)

        # create two order with same shelf life and decay rate
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=300, decayRate=0.45)
        hot_order2 = Order(id="2", name="Pizza", temp=Temp.HOT, shelfLife=300, decayRate=0.45)

        # put first order in the allowable shelf
        shelf_manager.put_order(hot_order1)
        # put second order in the overflow shelf
        shelf_manager.put_order(hot_order2)

        # mock the clock tick event
        event = threading.Event()
        threading.Thread(target=shelf_manager.init_manager_thread, args=(event,),daemon=True).start()
        event.set()
        time.sleep(0.01)

        # Expect: after clock interval, each order receive different inherent_value in different shelves
        self.assertEqual(shelf_manager.peek_allowable_shelf(Temp.HOT)[0].inherent_value, 0.855)
        self.assertEqual(shelf_manager.peek_overflow_shelf()[0].inherent_value, 0.81)

unittest.main()
