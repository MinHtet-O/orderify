from sre_constants import ANY
import unittest
from shelf import *
from shelf_manager import *

# Define 3 allowable shelves with size of 1. and overflow shelves with size of 2
# put order with "HOT" temp
# put order with "FROZEN" temp
# put order with "COLD" temp
# expected: each order is in respective shelf

class ShelfManagerTest(unittest.TestCase):
    def setUp(self):
        
        hot_shelf = Shelf(1, ShelfTemp.HOT)
        cold_shelf = Shelf(1, ShelfTemp.COLD)
        frozen_shelf = Shelf(1, ShelfTemp.FROZEN)
        overflow_shelf = Shelf(2, None)

        self.shelf_manager = ShelfManager(
            allowable_shelves= {
                ShelfTemp.HOT: hot_shelf,
                ShelfTemp.COLD: cold_shelf,
                ShelfTemp.FROZEN: frozen_shelf
            },
            overflow_shelf = overflow_shelf
        )

    def test_order_placement(self):
        hot_order1 = Order(id="1", name="Pizza", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
        hot_order3 = Order(id="3", name="Burger", temp=ShelfTemp.HOT, shelfLife=1, decayRate=1)
        
        cold_order1 = Order(id="4", name="Smoothie", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
        cold_order2 = Order(id="5", name="Pepsi", temp=ShelfTemp.COLD, shelfLife=1, decayRate=1)
        frozen_order = Order(id="6", name="Ice Cream", temp=ShelfTemp.FROZEN, shelfLife=1, decayRate=1)
        
        self.shelf_manager.put_order(hot_order1)
        self.shelf_manager.put_order(cold_order1)
        self.shelf_manager.put_order(frozen_order)

        # Expect: each order are placed on the shelves with respective temperature
        self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.HOT), [hot_order1])
        self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.COLD), [cold_order1])
        self.assertEqual(self.shelf_manager.peek_orders(ShelfTemp.FROZEN), [frozen_order])

        self.shelf_manager.put_order(hot_order2)
        self.shelf_manager.put_order(hot_order3)

        # Expect: additional orders are stored in the overflow shelf
        self.assertEqual(self.shelf_manager.peek_orders(None), [hot_order2, hot_order3])

        #Except: True, all shelves are full
        self.assertEqual(self.shelf_manager.check_shelves_full(), True)

        # Expect: unable to accept any order.
        with self.assertRaises(NoEmptySpaceErr):
            self.shelf_manager.put_order(cold_order2)

unittest.main()

# update 1 order value to -1
# update 1 order status to delivered

# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : orders with status delivered (or) value less than 0 are removed

# put 1 order in HOT, 1 order in FROZEN, 2 order in overflow shelves
# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : 1 COLD item from overflow shelves is put back to COLD allowable shelves

# put 1 order in HOT, 1 order in FROZEN,1 order in COLD and 2 order in overflow shelves
# after SHELF_MANAGEMENT_INTERVAL sec,
# expected : random item from overflow sheles is dropped