# Orderify

## About the system

Orderify is the real-time system that emulates the fulfilment of delivery orders for a kitchen. The kitchen will instantly cook the order upon receiving it, and then place the order on the best-available shelf (see Shelves section) to await pick up by a waiter.
- Upon receiving an order, the system should dispatch a courier to pick up and deliver that specific order.
- The courier should arrive randomly between 2-6 seconds later. The courier should instantly pick up the order upon arrival. Once an order is picked up, the courier should instantly deliver it.
- Each order should be placed on a shelf that matches the order!s temperature. If that shelf is full, an order can be placed on the overflow shelf. If the overflow shelf is full, git existing order of your choosing on the overflow should be moved to an allowable shelf with the room
- Orders have an inherent value that will deteriorate over time, based on the order!s shelfLife and decayRate fields. Orders that have reached a value of zero are considered wasted: they should never be delivered and should be removed from the shelf.

## Setup instructions
1. Download and install [python3](https://www.python.org/downloads/) on your machine.
2. Clone the project and get into the root directory <br>```git clone https://github.com/MinHtet-O/orderify.git && cd orderify```
3. Install dependencies <br>```pip3 install -r requirements.txt```
4. Run the tests <br>```python3 -m unittest```
5. Run the app <br>```python3 main.py```

For Unix/ Linux system, you can install dependencies, tests and run app in one command.<br>```make test```

## Architecture Diagram
![alt text](https://github.com/MinHtet-O/orderify/blob/main/resources/diagrams/3_final_after_refactoring.png)

## Component Description

### Kitchen
Kitchen acts as the central orchestrator between the order client, courier, and pickup manager.
It serves the API handlers, dispatches the delivery, and maintains a list of orders.
The orders are stored in the hash map of `````[ order_id ] -> Order````` for fast retrieval of the orders for kitchen handlers.

But if we have requirements like getting all orders in the current system, it would be inefficient to iterate 
the hash map for each order within the system. Also, it's not memory efficient to hold all the orders in the hash map compared to list. 
As an improvement, the orders which are already failed or have been delivered should be moved to the list as archived orders.

### Shelf
Shelf is the basic data storage for the pickup area. Each shelf maintains it's own decay modifier.
There are normal overflow shelf and shelves with temperatures, which can only store the order of the same temperature.
Each shelf can only store the orders up to its maximum capacity size.

### Pickup Area
Pickup Area is the main data structure that interacts with kitchen for the shelf management.
Each pickup area can hold one overflowshelf and multiple allowable shelves with a specific temperature.
Although it maintains two separate data stores internally, the complexity is hidden and shelf/ order iterators are exposed for shelf policies.

### Order

Data class to store each individual order. The status, order age, and inherent value ( deterioration value) will be changed during the order life cycle.
The status can only be changed from one permitted state to another. There is the internal thread lock for concurrency control for each order.
Currently, it's a regular thread lock. But it should be replaced with read/write lock for better performance as a further improvement.

### Shelf Policies

Shelf Policies are applied to each shelf through pickup area.
Those policies can be removed, changed in order, or replaced individually during run time.
Currently, there are only four policies that
- calculate and update deterioration for each order
- discard spoiled orders
- discard random order if all shelves are full
- move order from one shelf to another
  Additional policies can be implemented through ShelfPolicy interface.

### Courior

Courier manager receives the delivery order through the delivery queue for asynchronous communication.
In further system, there could be multiple queues based on the address/ region of the order and each courier scheduler
will only listen to its specific queue.
Upon receiving the order, it waits for a random duration ( to stimulate the pickup duration ) before
it pickup and sends a delivered message to the kitchen. The order is instantly delivered.
