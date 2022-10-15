import unittest
from order.order import  Order, OrderStatus, Temp
from errors import InvalidOrderStatus, InvalidOrderInherentValue
from config import ORDER_AGE_INC

class OrderTest(unittest.TestCase):
    def setUp(self):
        self.order = Order("1", "Pizza",Temp.HOT,300,0.45)

    def test_update_status(self):
        # Expect: initial state pending
        self.assertEqual(self.order.status, OrderStatus.PENDING)

        # Expect: unable to change state directly from PENDING to DELIVERED
        with self.assertRaises(InvalidOrderStatus):
            self.order.status = OrderStatus.DELIVERED

        self.order.status = OrderStatus.WAITING
        # Expect: order status has changed to WAITING
        self.assertEqual(self.order.status, OrderStatus.WAITING)
        self.order.status = OrderStatus.DELIVERED
        self.assertTrue(self.order.delivered())

        with self.assertRaises(InvalidOrderStatus):
            self.order.status = OrderStatus.FAILED

    def test_update_order_age(self):
        # Expect: initial order age is zero
        self.assertEqual(self.order.order_age, 0)
        self.order.inc_order_age()
        # Expect: increment order age
        self.assertEqual(self.order.order_age, ORDER_AGE_INC)
        self.order.inc_order_age()
        # Expect: increment order age
        self.assertEqual(self.order.order_age, ORDER_AGE_INC*2)

        #Expect: unable to set order age directly
        with self.assertRaises(AttributeError):
            self.order.order_age = -1

    def test_update_inherent_value(self):
      self.assertEqual(self.order.inherent_value, 1)
      # Expect: the new inherent value must smaller than current
      with self.assertRaises(InvalidOrderInherentValue):
          self.order.inherent_value = 2

      self.order.inherent_value = -1
      # Expect :order is spoiled
      self.assertEqual(self.order.inherent_value, -1)
      self.assertTrue(self.order.spoiled())
