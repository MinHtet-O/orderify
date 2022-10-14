
# state transition
import unittest
from errors import *
from order import *
from temp import *

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
        self.assertEqual(self.order.status, OrderStatus.DELIVERED)

        with self.assertRaises(InvalidOrderStatus):
            self.order.status = OrderStatus.FAILED

    def test_update_order_age(self):
        self.order.order_age = 10

        #Expect: the new order age must greather than current
        with self.assertRaises(InvalidOrderAge):
            self.order.order_age = 5

    def test_update_inherent_value(self):
      self.assertEqual(self.order.inherent_value, 1)
      # Expect: the new inherent value must smaller than current
      with self.assertRaises(InvalidOrderInherentValue):
          self.order.inherent_value = 2

unittest.main()
