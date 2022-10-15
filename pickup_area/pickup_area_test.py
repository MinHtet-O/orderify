import unittest
from pickup_area.pickup_area import PickupArea, Order
from errors import ShelfAlreadyExits, NoEmptySpaceErr, InvalidOrderID
from order.order import Temp


class PickupAreaTest(unittest.TestCase):
    def setUp(self):
        self.pickup_area = PickupArea()
        self.pickup_area.add_allowable_shelf(1, Temp.HOT)
        self.pickup_area.add_allowable_shelf(1, Temp.COLD)
        self.pickup_area.add_allowable_shelf(1, Temp.FROZEN)
        self.pickup_area.add_overflow_shelf(2)

    def test_shelf_placement(self):
        # Expect: unable to add another allowable shelf of the existing Temp
        with self.assertRaises(ShelfAlreadyExits):
            self.pickup_area.add_allowable_shelf(1, Temp.HOT)
        with self.assertRaises(ShelfAlreadyExits):
            self.pickup_area.add_allowable_shelf(1, Temp.FROZEN)
        # Expect: unable to add another overflow shelf
        with self.assertRaises(ShelfAlreadyExits):
            self.pickup_area.add_overflow_shelf(2)

    def test_remove_order(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        self.pickup_area.put_order(hot_order1)
        # Expect: order with id 1 is in the Hot shelf
        self.assertTrue(hot_order1 in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)
        self.pickup_area.remove_order("1")
        # Expect: order with id 1 is removed from HOT shelf
        self.assertFalse(hot_order1 in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)

        # Expect: unable to remove order that doesn't exit
        with self.assertRaises(InvalidOrderID):
            self.pickup_area.remove_order("999")

    def test_order_placement(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        hot_order3 = Order(id="3", name="Burger", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        cold_order1 = Order(id="4", name="Smoothie", temp=Temp.COLD, shelf_life=1, decay_rate=1)
        cold_order2 = Order(id="5", name="Pepsi", temp=Temp.COLD, shelf_life=1, decay_rate=1)
        frozen_order = Order(id="6", name="Ice Cream", temp=Temp.FROZEN, shelf_life=1, decay_rate=1)

        # Put three order
        self.pickup_area.put_order(hot_order1)
        self.pickup_area.put_order(cold_order1)
        self.pickup_area.put_order(frozen_order)

        # Expect: each order are placed on the shelves with respective temperature
        self.assertEqual(self.pickup_area.get_allowable_shelf(Temp.HOT).orders, [hot_order1])
        self.assertEqual(self.pickup_area.get_allowable_shelf(Temp.COLD).orders, [cold_order1])
        self.assertEqual(self.pickup_area.get_allowable_shelf(Temp.FROZEN).orders, [frozen_order])

        # Put two more order
        self.pickup_area.put_order(hot_order2)
        self.pickup_area.put_order(hot_order3)

        # Expect: additional orders are stored in the overflow shelf
        self.assertEqual(self.pickup_area.overflow_shelf.orders, [hot_order2, hot_order3])

        # Except:all shelves are full
        self.assertTrue(self.pickup_area.all_shelves_full())

        # put one more order
        self.pickup_area.put_order(cold_order2)
        # Expect: unable to accept any order.
        self.assertIsInstance(self.pickup_area.put_order(cold_order2), NoEmptySpaceErr)
