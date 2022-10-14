def calc_inherent_value(shelf_life, order_age, decay_rate,decay_mod) -> float:
    value = (shelf_life - order_age - decay_rate* (order_age*decay_mod))/ shelf_life
    value = (round(value,8))
    return value
