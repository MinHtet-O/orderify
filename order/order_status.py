from enum import Enum
from errors import InvalidOrderError


class OrderStatus(str, Enum):

    PENDING = "PENDING" # pending to be accepted from kitchen
    WAITING = "WAITING" # cooked and waiting for delivery
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    REJECTED = "REJECTED" # rejected from the kitchen

    @staticmethod
    def decode_json(json):
        if not 'status' in json:
            raise InvalidOrderError("status should not be empty")
        status = json['status'].upper()
        try:
            status = OrderStatus[status]
        except Exception as e:
            raise InvalidOrderError("{} is not valid status".format(status))
        return status

StatusTrans = {
    # from : to
    OrderStatus.PENDING: [OrderStatus.WAITING, OrderStatus.FAILED, OrderStatus.REJECTED],
    OrderStatus.WAITING: [OrderStatus.DELIVERED, OrderStatus.FAILED]
}
