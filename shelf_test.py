import unittest
from shelf import *

class MyFirstTests(unittest.TestCase):
    def test_food_inherent_value(self):
        test_data = [
            #shelf_life, decay_rate, age, shelfdecay, value
            (300, 0.45, 1, 2, 0.99366667),
            (300, 0.45, 2, 2, 0.98733333),
            (300, 0.45, 3, 2, 0.981),
            (300, 0.45, 4, 2, 0.97466667),
        ]

        for data in test_data:
            value = get_inherent_value(
            shelf_life= data[0],
            decay_rate= data[1],
            order_age= data[2],
            decay_mod=data[3]
            )
            self.assertEqual(value, data[4])
        

unittest.main()