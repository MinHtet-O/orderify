from time import sleep, time
from shelf import *
import threading

# TODO: add status field to Order

class ShelfManager:
    def __init__(self, allowable_shelves: list[Shelf], overflow_shelf: Shelf):
        self.allowable_shelves = allowable_shelves
        self.overflow_shelf = overflow_shelf
        threading.Thread(target=self.__update_order_age).start()

    def put_order(self, order: Order):
        # put order on in the allowable shelve with respective temp
        for shelf in self.allowable_shelves:
            if shelf.temp == order.temp:
                err = shelf.put_order(order)
                if err == NoEmptySpace:
                    raise err
                return
        # put order in the overflow shelf
        err = self.overflow_shelf(order)
        if err == NoEmptySpace:
            raise err
        
        
    def check_shelves_full(self):
        full = False
        for shelf in self.allowable_shelves:
            full = shelf.check_full()
        full = self.overflow_shelf.check_full()
        return full

    def __update_order_age(self):
        # initialize the thread to update order age every x second
        while True:
            time.sleep(1)
            self.update_deterioration()
        

    def remove_order(self):
        pass

    def update_deterioration(self):
        #list through items and update deterioration value
        for shelf in self.allowable_shelves:
            shelf.update_deterioration()
        self.overflow_shelf.update_deterioration()
        

