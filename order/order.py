import threading, json
from config import ORDER_AGE_INC
from errors import InvalidOrderStatus, InvalidOrderInherentValue, InvalidOrderError
from order.order_status import OrderStatus, StatusTrans
from order.temp import Temp


def lock_attr(func):
    def wrapper(*args, **kwargs):
        with args[0].lock:
            return func(*args, **kwargs)

    return wrapper


class Order:
    def __init__(self, id: str, name: str, temp: Temp, shelf_life: int, decay_rate: float):
        self.__id = id
        self.__name = name
        self.__temp = temp
        self.__shelf_life = shelf_life
        self.__decay_rate = decay_rate
        self.__status = OrderStatus.PENDING
        self.__order_age = 0
        self.__inherent_value = 1
        self.lock = threading.Lock()

    def spoiled(self) -> bool:
        return self.inherent_value < 0

    def delivered(self) -> bool:
        return self.status == OrderStatus.DELIVERED

    def __verify_status_trans(self, current: OrderStatus, next: OrderStatus) -> bool:
        if current not in StatusTrans:
            return False
        valid_states = StatusTrans[current]
        return next in valid_states

    def __verify_inherent_value_trans(self, current: int, new: int) -> bool:
        return new < current

    def __repr__(self):
        order_str = "ID: {}, name: {}, temp: {}, value: {}, order_age {}".format(
            self.__id,
            self.__name,
            self.__temp,
            self.__inherent_value,
            self.__order_age
        )
        return order_str

    def inc_order_age(self) -> None:
        self.__order_age += ORDER_AGE_INC

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def decode_json(json):
        # TODO: refactor as custom validator method
        if 'id' not in json:
            raise InvalidOrderError("there is no id field")
        if 'name' not in json:
            raise InvalidOrderError("there is no name field")
        if 'temp' not in json:
            raise InvalidOrderError("there is no temp field")
        if 'shelfLife' not in json:
            raise InvalidOrderError("there is no shelfLife field")
        if 'decayRate' not in json:
            raise InvalidOrderError("there is no decayRate field")

        temp = json["temp"].upper()
        id = json["id"]
        name = json["name"]
        temp: Temp = Temp[temp]
        shelf_life = json["shelfLife"]
        decay_rate = json["decayRate"]

        order = Order(id, name, temp, shelf_life, decay_rate)
        return order

    @property
    @lock_attr
    def id(self):
        return self.__id

    @id.setter
    @lock_attr
    def id(self, id):
        self.__id = id

    @property
    @lock_attr
    def name(self):
        return self.__name

    @name.setter
    @lock_attr
    def name(self, name):
        self.__name = name

    @property
    @lock_attr
    def temp(self):
        return self.__temp

    @temp.setter
    @lock_attr
    def temp(self, temp):
        self.__temp = temp

    @property
    @lock_attr
    def shelf_life(self):
        return self.__shelf_life

    @shelf_life.setter
    @lock_attr
    def shelf_life(self, shelf_life):
        self.__shelf_life = shelf_life

    @property
    @lock_attr
    def decay_rate(self):
        return self.__decay_rate

    @decay_rate.setter
    @lock_attr
    def decay_rate(self, decay_rate):
        self.__decay_rate = decay_rate

    @property
    @lock_attr
    def status(self):
        return self.__status

    @status.setter
    @lock_attr
    def status(self, status):
        if not self.__verify_status_trans(current=self.__status, next=status):
            raise InvalidOrderStatus("can not change order to {} which is already {}".format(status, self.__status))
        self.__status = status

    @property
    @lock_attr
    def order_age(self):
        return self.__order_age

    @property
    @lock_attr
    def inherent_value(self):
        return self.__inherent_value

    @inherent_value.setter
    @lock_attr
    def inherent_value(self, inherent_value):
        if not self.__verify_inherent_value_trans(current=self.__inherent_value, new=inherent_value):
            raise InvalidOrderInherentValue(f"""can not set inherent {inherent_value} 
            which is bigger than current {self.__inherent_value} for {self.__name}""")
        print("{} value is about to update to {}".format(self.__name, inherent_value))
        self.__inherent_value = inherent_value


class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        data = dict()
        data['id'] = obj.id
        data['name'] = obj.name
        data['status'] = obj.status
        return data
