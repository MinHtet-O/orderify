shel_life = 300
order_age = 16
decay_rate = 0.45
decay_mod = 2


value = (shel_life - order_age - decay_rate* (order_age*decay_mod))/ shel_life
value = (round(value,8))
print(value)
