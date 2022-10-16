from order.temp import Temp

API_URL = "http://127.0.0.1:5000"

# courior
MIN_DELIVER_DURATION = 2
MAX_DELIVER_DURATION = 6

# order client
ORDER_CLIENT_INTERVAL = 2

# shelf
allowable_shelf_size = 10
overflow_shelf_size = 15
ALLOWABLE_DECAY_MODS = {
    Temp.HOT: 1,
    Temp.COLD: 1,GIT
    Temp.FROZEN: 1,

}
OVERFLOW_DECAY_MODS = 2

# order_age of each order will increase by ORDER_AGE_INC continuously
ORDER_AGE_INC = 30

# shelf management
SHELF_POLICY_INTERVAL = 1

# TODO: read config from yaml
