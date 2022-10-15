import unittest
from shelf.calc_inherent import calc_inherent_value
from shelf.shelf import Shelf
from shelf.temp_shelf import TempShelf
from order.order import Order, Temp
from errors import TempNotMatchErr, NoEmptySpaceErr


class ShelfTest(unittest.TestCase):
    def setUp(self):
        self.overflow_shelf: Shelf = Shelf(capacity=2)

    def prepare_orders(self):
        # define external helper method to generate test dta
        order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        order3 = Order(id="3", name="Burger", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        return order1, order2, order3

    def test_put_orders(self):
        order1, order2, order3 = self.prepare_orders()
        self.overflow_shelf.put_order(order1)
        self.overflow_shelf.put_order(order2)

        # Expect: the two orders are in the list
        self.assertTrue(order1 in self.overflow_shelf.orders)
        self.assertTrue(order2 in self.overflow_shelf.orders)

        # Expect: unable to mutate orders directly
        with self.assertRaises(AttributeError):
            self.overflow_shelf.orders = [order3]

    def test_temp_match(self):
        hot_shelf: Shelf = TempShelf(capacity=2, temp=Temp.HOT)
        cold_order = Order(id="1", name="Ice Cream", temp=Temp.FROZEN, shelf_life=1, decay_rate=1)
        hot_order = Order(id="2", name="Noodle", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        # Expect: unable to accept order of different temp
        with self.assertRaises(TempNotMatchErr):
            hot_shelf.put_order(cold_order)

        hot_shelf.put_order(hot_order)
        # Expect: hot order in self.hot_shelf.orders
        self.assertTrue(hot_order in hot_shelf.orders)

    def test_storage_capacity(self):
        order1, order2, order3 = self.prepare_orders()

        # put two orders to the shelf
        self.overflow_shelf.put_order(order1)
        self.overflow_shelf.put_order(order2)

        # Expect: shelf is full
        self.assertTrue(self.overflow_shelf.full())

        # Expect: unable to accept order anymore
        with self.assertRaises(NoEmptySpaceErr):
            self.overflow_shelf.put_order(order3)

        # remove order2
        self.overflow_shelf.remove_order(1)

        # Expect: shelf is no longer full
        self.assertFalse(self.overflow_shelf.full())

        # Expect: only order 1 exits in the shelf at the end
        self.assertEqual(self.overflow_shelf.orders, [order1])


class CalcInherentValueTest(unittest.TestCase):
    def test_food_inherent_value(self):
        test_data = [
            # shelf_life, decay_rate, age, shelf decay, value
            (300, 0.45, 1, 2, 0.99366667),
            (300, 0.45, 2, 2, 0.98733333),
            (300, 0.45, 3, 2, 0.981),
            (300, 0.45, 4, 2, 0.97466667),
        ]

        for data in test_data:
            value = calc_inherent_value(
                shelf_life=data[0],
                decay_rate=data[1],
                order_age=data[2],
                decay_mod=data[3]
            )
            self.assertEqual(value, data[4])
