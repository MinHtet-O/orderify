from typing import Counter
import threading
import random

rand = random.randrange(2, 3)
print(rand)

class CustomClass:
    def __init__(self):
        self.num = 0
        self.lock = threading.Lock()

    def set_number(self, num):
        with self.lock:
            self.num = num

obj1 = CustomClass()
obj2 = CustomClass()    
objects = {
    "obj1": obj1,
    "obj2": obj2
}

# def method_1(obj):
#     obj.lock.acquire()

# def method_2(obj):
#     obj.set_number(2)

# threading.Thread(target=method_1, args=(objects["obj1"],)).start()
# threading.Thread(target=method_2, args=(objects["obj2"],)).start()
# time.sleep(1)
# print(obj1.num)
# print(obj2.num)

