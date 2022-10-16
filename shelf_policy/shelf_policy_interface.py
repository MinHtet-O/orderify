from abc import ABC, abstractmethod
from pickup_area.pickup_area import PickupArea

class ShelfPolicy(ABC):

    @abstractmethod
    def apply_policy(self, pickup_area: PickupArea):
        pass







