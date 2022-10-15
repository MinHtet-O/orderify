import time, unittest, threading
from order.order import Temp, Order, OrderStatus
from pickup_area.pickup_area import  PickupArea
from shelf_manager.shelf_manager import ShelfManager
from errors import InvalidOrderID, ShelfManagerAssignedAlready

from shelf_manager import *

def tickEvent(event: threading.Event):
    event.set()
    time.sleep(0.01)

class ShelfManagerTest(unittest.TestCase):
    def setUp(self):
        pickup_area = PickupArea()
        self.shelf_manager = ShelfManager()
        pickup_area.add_allowable_shelf(1, Temp.HOT)
        pickup_area.add_allowable_shelf(1, Temp.COLD)
        pickup_area.add_allowable_shelf(1, Temp.FROZEN)
        pickup_area.add_overflow_shelf(2)
        self.pickup_area = self.shelf_manager.assign(pickup_area)

        # mock clock tick interval
        self.manage_shelf_event = threading.Event()
        threading.Thread(target=self.shelf_manager.manage_shelves,
                         args=(self.manage_shelf_event,),
                         daemon=True).start()

    def test_assign_pickup_area(self):
        pickup_area_2 = PickupArea
        # Expect: unable to assign another pickup area
        with self.assertRaises(ShelfManagerAssignedAlready):
            self.shelf_manager.assign(pickup_area_2)

    def test_remove_order_if_full(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=1, decayRate=1)
        cold_order1 = Order(id="3", name="Smoothie", temp=Temp.COLD, shelfLife=1, decayRate=1)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelfLife=1, decayRate=1)
        frozen_order = Order(id="5", name="Ice Cream", temp=Temp.FROZEN, shelfLife=1, decayRate=1)

        # put 1 order in each allowable shelves
        self.pickup_area.put_order(hot_order1)
        self.pickup_area.put_order(cold_order1)
        self.pickup_area.put_order(frozen_order)
        # put 2 orders in overflow shelves
        self.pickup_area.put_order(hot_order2)
        self.pickup_area.put_order(cold_order2)

        # Expect: overflow shelf becomes full
        self.assertEqual(len(self.pickup_area.overflow_shelf.orders), 2)

        # trigger clock tick
        tickEvent(self.manage_shelf_event)

        # Expect: random order has dropped from overflow shelves
        # Expect: now overflow shelf has only one order
        self.assertEqual(len(self.pickup_area.overflow_shelf.orders), 1)

    def test_order_replacement(self):
        perishable_order = Order(id="1", name="Perishable Pizza", temp=Temp.HOT, shelfLife=300, decayRate=20)
        hot_order = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=300, decayRate=0.45)
        cold_order1 = Order(id="4", name="Smoothie", temp=Temp.COLD, shelfLife=300, decayRate=0.45)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelfLife=300, decayRate=0.45)
        frozen_order = Order(id="6", name="Ice Cream", temp=Temp.FROZEN, shelfLife=300, decayRate=0.45)

        # put 1 order in each allowable shelves
        self.pickup_area.put_order(perishable_order)
        self.pickup_area.put_order(cold_order1)
        self.pickup_area.put_order(frozen_order)

        # put 2 orders in overflow shelves, overflow shelf is full
        self.pickup_area.put_order(hot_order)
        self.pickup_area.put_order(cold_order2)
        self.assertTrue(self.pickup_area.overflow_shelf.full())

        # trigger clock tick
        tickEvent(self.manage_shelf_event)

        # Expect: discarded spoiled order
        self.assertFalse(perishable_order in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)
        # Expect: spoiled order status becomes FAILED
        self.assertEqual(perishable_order.status, OrderStatus.FAILED)

        # Expect: The overflow shelf is full and temp shelf is free
        # hot_order is moved to allowable shelf
        self.assertTrue(hot_order in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)
        # hot_order is no longer in overflow shelf
        self.assertFalse(hot_order in self.pickup_area.overflow_shelf.orders)

    def test_deterioration_overtime(self):

        # create two order with same shelf life and decay rate
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=300, decayRate=0.45)
        hot_order2 = Order(id="2", name="Pizza", temp=Temp.HOT, shelfLife=300, decayRate=0.45)

        # put first order in the allowable shelf
        self.pickup_area.put_order(hot_order1)
        # put second order in the overflow shelf
        self.pickup_area.put_order(hot_order2)

        # trigger clock tick
        tickEvent(self.manage_shelf_event)

        # Expect: after clock interval, each order receive different inherent_value in different shelves
        self.assertEqual(self.pickup_area.get_allowable_shelf(Temp.HOT).orders[0].inherent_value, 0.855)
        self.assertEqual(self.pickup_area.overflow_shelf.orders[0].inherent_value, 0.81)

