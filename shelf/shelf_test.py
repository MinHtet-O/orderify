import unittest
from shelf.calc_inherent import *


class ShelfTest(unittest.TestCase):
    def setUp(self):
        self.shelf: Shelf = Shelf(capacity= 2, temp=Temp.HOT)

    def prepare_orders(self):
        # define external helper method to generate test dta
        order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelfLife=1, decayRate=1)
        order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelfLife=1, decayRate=1)
        order3 = Order(id="3", name="Burger", temp=Temp.HOT, shelfLife=1, decayRate=1)
        return (order1,order2,order3)

    def test_get_orders(self):
        order1, order2, _ = self.prepare_orders()
        self.shelf.put_order(order1)
        self.shelf.put_order(order2)

        # Expect: the two orders are in the list
        self.assertEqual(self.shelf.get_orders(), [order1,order2])

    def test_temp_not_match(self):
        invalid_order = Order(id="1", name="Ice Cream", temp=Temp.FROZEN, shelfLife=1, decayRate=1)
        # Expect: unable to accept order of different temp
        with self.assertRaises(TempNotMatchErr):
            self.shelf.put_order(invalid_order)

    def test_storage_capacity(self):
        order1, order2, order3 = self.prepare_orders()

        # put two orders to the shelf
        self.shelf.put_order(order1)
        self.shelf.put_order(order2)

        # Expect: shelf is full
        self.assertEqual(self.shelf.full(), True)

        # Expect: unable to accept order anymore
        with self.assertRaises(NoEmptySpaceErr):
            self.shelf.put_order(order3)

        # remove order2
        self.shelf.remove_order(1)

        # Expect: shelf is no longer full
        self.assertEqual(self.shelf.full(), False)

        # Expect: only order 1 exits in the shelf at the end
        self.assertEqual(self.shelf.get_orders(), [order1])

class CalcInherentValueTest(unittest.TestCase):
    def test_food_inherent_value(self):
        test_data = [
            #shelf_life, decay_rate, age, shelfdecay, value
            (300, 0.45, 1, 2, 0.99366667),
            (300, 0.45, 2, 2, 0.98733333),
            (300, 0.45, 3, 2, 0.981),
            (300, 0.45, 4, 2, 0.97466667),
        ]

        for data in test_data:
            value = calc_inherent_value(
            shelf_life= data[0],
            decay_rate= data[1],
            order_age= data[2],
            decay_mod=data[3]
            )
            self.assertEqual(value, data[4])

unittest.main()
