from time import sleep
from pickup_area.pickup_area import PickupArea
import random
from order.order import Order, OrderStatus
from errors import ShelfManagerAssignedAlready
from typing import Optional
from shelf_policy.shelf_policy_interface import ShelfPolicy
from config import SHELF_POLICY_INTERVAL

class ShelfPolicyAggregator:
    def __init__(self, *args: ShelfPolicy):
        self.__shelf_policies = args

    def assign(self, pickup_area: PickupArea) -> PickupArea:
        if self.__pickup_area is not None:
            raise ShelfManagerAssignedAlready("unable to assign to more than one pickup area")
        self.__pickup_area = pickup_area
        return pickup_area

    def apply_policies_per_interval(self, pickup_area) -> None:
        if len(self.__shelf_policies) == 0:
            print("PolicyAggregator: no policy to apply")
            return
        while True:
            sleep(SHELF_POLICY_INTERVAL)
            self.__apply_policies(self, pickup_area)


    def __apply_policies(self, event, pickup_area) -> None:
         for policy in self.__shelf_policies:
               policy.apply_policy(pickup_area)




