from enum import Enum

from errors import InvalidOrderError
from order.order_status import OrderStatus


class Temp(str, Enum):
    HOT = "HOT"
    COLD = "COLD"
    FROZEN = "FROZEN"

    @staticmethod
    def decode_json(json):
        temp = json['temp'].upper()
        try:
            temp = OrderStatus[temp]
        except Exception as e:
            raise InvalidOrderError("{} is not valid temp".format(temp))
        return temp
