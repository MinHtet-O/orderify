import time, unittest, threading
from order.order import Temp, Order, OrderStatus
from pickup_area.pickup_area import PickupArea
from shelf_policy.policy_aggregator import ShelfPolicyAggregator
from errors import InvalidOrderID, ShelfManagerAssignedAlready
from shelf_policy import OnFullOrderRemover, OrderRelocator, OrderDeteriorator, SpoiledOrderRemover

class ShelfPoliciesTest(unittest.TestCase):
    def setUp(self):
        self.pickup_area = PickupArea()
        self.pickup_area.add_allowable_shelf(1, Temp.HOT)
        self.pickup_area.add_allowable_shelf(1, Temp.COLD)
        self.pickup_area.add_allowable_shelf(1, Temp.FROZEN)
        self.pickup_area.add_overflow_shelf(2)

        # init policies
        self.onfull_order_remover = OnFullOrderRemover()
        self.order_relocator = OrderRelocator()
        self.order_deteriorator = OrderDeteriorator()
        self.spoiled_order_remover = SpoiledOrderRemover()

    def test_remove_order_if_full(self):
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        hot_order2 = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelf_life=1, decay_rate=1)
        cold_order1 = Order(id="3", name="Smoothie", temp=Temp.COLD, shelf_life=1, decay_rate=1)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelf_life=1, decay_rate=1)
        frozen_order = Order(id="5", name="Ice Cream", temp=Temp.FROZEN, shelf_life=1, decay_rate=1)

        # put 1 order in each allowable shelves
        self.pickup_area.put_order(hot_order1)
        self.pickup_area.put_order(cold_order1)
        self.pickup_area.put_order(frozen_order)
        # put 2 orders in overflow shelves
        self.pickup_area.put_order(hot_order2)
        self.pickup_area.put_order(cold_order2)

        # Expect: overflow shelf becomes full
        self.assertEqual(len(self.pickup_area.overflow_shelf.orders), 2)

        # apply remove order if full
        self.onfull_order_remover.apply_policy(self.pickup_area)

        # Expect: random order has dropped from overflow shelves
        # Expect: now overflow shelf has only one order
        self.assertEqual(len(self.pickup_area.overflow_shelf.orders), 1)

    #TODO: refactor into separate tests
    def test_order_relocate(self):
        perishable_order = Order(id="1", name="Perishable Pizza", temp=Temp.HOT, shelf_life=300, decay_rate=20)
        hot_order = Order(id="2", name="Hot Dog", temp=Temp.HOT, shelf_life=300, decay_rate=0.45)
        cold_order1 = Order(id="4", name="Smoothie", temp=Temp.COLD, shelf_life=300, decay_rate=0.45)
        cold_order2 = Order(id="4", name="Pepsi", temp=Temp.COLD, shelf_life=300, decay_rate=0.45)
        frozen_order = Order(id="6", name="Ice Cream", temp=Temp.FROZEN, shelf_life=300, decay_rate=0.45)

        # put 1 order in each allowable shelves
        self.pickup_area.put_order(perishable_order)
        self.pickup_area.put_order(cold_order1)
        self.pickup_area.put_order(frozen_order)

        # put 2 orders in overflow shelves, overflow shelf is full
        self.pickup_area.put_order(hot_order)
        self.pickup_area.put_order(cold_order2)
        self.assertTrue(self.pickup_area.overflow_shelf.full())

        # apply update order deterioration
        self.order_deteriorator.apply_policy(self.pickup_area)
        # Expect: the order has spoiled
        self.assertEqual(perishable_order.inherent_value, -1.1)
        # apply discard spoiled orders
        self.spoiled_order_remover.apply_policy(self.pickup_area)
        # Expect: discarded spoiled order
        self.assertFalse(perishable_order in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)
        # Expect: spoiled order status becomes FAILED
        self.assertEqual(perishable_order.status, OrderStatus.FAILED)

        # apply policy to relocate order from overflow to allowable
        self.order_relocator.apply_policy(self.pickup_area)
        # Expect: hot_order is relocated to allowable shelf
        self.assertTrue(hot_order in self.pickup_area.get_allowable_shelf(Temp.HOT).orders)
        # Expect: hot_order is no longer in overflow shelf
        self.assertFalse(hot_order in self.pickup_area.overflow_shelf.orders)

    def test_different_deterioration_rate_for_shelves(self):
        # create two order with same shelf life and decay rate
        hot_order1 = Order(id="1", name="Pizza", temp=Temp.HOT, shelf_life=300, decay_rate=0.45)
        hot_order2 = Order(id="2", name="Pizza", temp=Temp.HOT, shelf_life=300, decay_rate=0.45)

        # put first order in the allowable shelf
        self.pickup_area.put_order(hot_order1)
        # put second order in the overflow shelf
        self.pickup_area.put_order(hot_order2)

        # apply update order deterioration
        self.order_deteriorator.apply_policy(self.pickup_area)

        # Expect: after clock interval, each same order receive different inherent_value for different shelves
        self.assertEqual(self.pickup_area.get_allowable_shelf(Temp.HOT).orders[0].inherent_value, 0.855)
        self.assertEqual(self.pickup_area.overflow_shelf.orders[0].inherent_value, 0.81)



    def test_food_inherent_value(self):
        test_data = [
            # shelf_life, decay_rate, age, shelf decay, value
            (300, 0.45, 1, 2, 0.99366667),
            (300, 0.45, 2, 2, 0.98733333),
            (300, 0.45, 3, 2, 0.981),
            (300, 0.45, 4, 2, 0.97466667),
        ]

        for data in test_data:
            value = self.order_deteriorator.calc_inherent_value(
                shelf_life=data[0],
                decay_rate=data[1],
                order_age=data[2],
                decay_mod=data[3]
            )
            self.assertEqual(value, data[4])
