def decor1(func):
    def inner():
        print("inside decor1")
        x = func()
        return x * x
    return inner

def decor(func):
    def inner():
        print("inside decor")
        x = func()
        return 2 * x
    return inner

@decor1
@decor
def num():
    return 10

print(num())
