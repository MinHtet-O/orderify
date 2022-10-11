list1 = [1,2,3]
list2 = [4,5,6]

def generator(list1, list2):
    for i in list1:
        yield (i, "hello")
    for j in list2:
        yield (j, "hello")

g = generator(list1, list2)
print(g)

for i in g:
    print(i)