from order import *



ALLOWABLE_DECAY_MODS = {
    ShelfTemp.HOT: 1,
    ShelfTemp.COLD: 1,
    ShelfTemp.FROZEN: 1,
}

OVERFLOW_DECAY_MODS = 2

class Shelf:
    def __init__(self, capacity: int, temp: ShelfTemp ):
        self.store: list[Order] = []
        self.capacity = capacity
        self.temp = temp
        if temp == None:
            self.decay_mod: int = OVERFLOW_DECAY_MODS
        else:
            self.decay_mod:int = ALLOWABLE_DECAY_MODS[temp]

    def occupied_storage(self):
        return len(self.store)

    def check_full(self):
        if len(self.store) >= self.capacity:
            return True
        return False

    def put_order(self, order: Order):
        if self.temp != order.temp: 
            raise TempNotMatchErr("order temp {} can not put in shelf with temp {}".format(order.temp, self.temp))
        if self.check_full():
            raise NoEmptySpaceErr("shelf has reached to it's max storage of {}".format(self.capacity))
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
            order.update_inherent_value(value)

    def remove_order(self, index):
        self.store.pop(index)
        pass

def calc_inherent_value(shelf_life, order_age, decay_rate,decay_mod):
    value = (shelf_life - order_age - decay_rate* (order_age*decay_mod))/ shelf_life
    value = (round(value,8))
    return value

class NoEmptySpaceErr(Exception):
    pass

class TempNotMatchErr(Exception):
    pass

# test: define shelf size of 2. 

# add 1 order with incorrect temperature 
# expected: raise error

# add 2 orders to the shelf.
# expected: shelf is full

# add 3 rd orders to the shelf
# expected: raise no empty space exception

# test: remove specific order
# expected: the order is no longer in the shelf

# test: check_full
# expected: false
