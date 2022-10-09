def courier(delivery_queue):
    print("waiting for queue")
    while True:
        order = delivery_queue.get()
        if order == None:
            print("All items delivered")
            break
        print(f'Delivering on {order.name}')