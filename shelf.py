from order import *



ALLOWABLE_DECAY_MODS = {
    ShelfTemp.HOT: 1,
    ShelfTemp.COLD: 1,
    ShelfTemp.FROZEN: 1,
}
OVERFLOW_DECAY_MODS = 2

class Shelf:
    def __init__(self, size: int, temp: ShelfTemp ):
        self.store: list[Order] = []
        self.size = size
        self.temp = temp
        if temp == None:
            self.decay_mod = OVERFLOW_DECAY_MODS
        else:
            self.decay_mod = ALLOWABLE_DECAY_MODS[temp].value

    def check_full(self):
        if len(self.store) >= self.size:
            return True
        return False

    def put_order(self, order: Order):
        if self.check_full():
            return NoEmptySpace("shelf has reached to it's max storage of {}".format(self.size))
        self.store.append(order)
        return None

    def drop_order(self, index: int):
        del self.store[index]

    def update_deterioration(self):
        for order in self.store:
            value = calc_inherent_value(
                shelf_life=order.shelf_life,
                order_age= order.order_age,
                decay_rate= order.decay_rate,
                decay_mod=self.decay_mod
            )
            order.inherent_value = value


def calc_inherent_value(shelf_life, order_age, decay_rate,decay_mod):
    value = (shelf_life - order_age - decay_rate* (order_age*decay_mod))/ shelf_life
    value = (round(value,8))
    return value

class NoEmptySpace(Exception):
    pass

# test: define shelf size of 5. add 6 orders to the shelf.
# expect: return error in 6th order
