# Order Errors
class InvalidOrderError(Exception):
    pass


class InvalidOrderID(Exception):
    pass


# Shelf Errors
class NoEmptySpaceErr(Exception):
    pass


class TempNotMatchErr(Exception):
    pass


# Shelf Management Errors
class ShelfAlreadyExits(Exception):
    pass


class ShelfManagerAssignedAlready(Exception):
    pass


# Order errors
class InvalidOrderStatus(Exception):
    pass


class InvalidOrderInherentValue(Exception):
    pass
