
# state transition
import unittest
from shelf import *

class OrderTest(unittest.TestCase):
    def setUp(self):
        self.order = Order("1", "Pizza",ShelfTemp.HOT,300,0.45)

    def test_update_status(self):
        print("before status update")
        self.order.status = OrderStatus.PENDING
        print("after status update")
        print(self.order.name)
        print(self.order.temp)
        print(self.order)

unittest.main()
