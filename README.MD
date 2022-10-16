# Orderify

#### Setup instructions
1. Download and install [python3](https://www.python.org/downloads/) on your machine.
2. Clone the project and get into the root directory <br>```git clone https://github.com/MinHtet-O/orderify.git && cd orderify```
3. Install dependencies <br>```pip3 install -r requirements.txt```
4. Run the tests <br>```python3 -m unittest```
5. Run the app <br>```python3 main.py```

For Unix/ Linux system, you can install dependencies, tests and run app in one command.<br>```make test```

#### Architecture Diagram
![alt text](https://github.com/MinHtet-O/orderify/blob/main/resources/diagrams/3_final_after_refactoring.png)

#### Component Description

### Kitchen
Kitchen acts as the central orchestrator between the order client, courior, and pickup manager.
It serves the API handlers, dispatch the delivery and maintains a list of orders. 
The orders are stored in the hash map of `````[ order_id ] -> Order````` for fast retrieval of the orders for kitchen handlers.

But if we have requirements like getting all orders in the current system, it would be inefficient to iterate the hash map for each order within the system. Also, it's not memory efficient to hold all the orders in the hash map.  As an improvement, the orders which are already failed or have been delivered should be moved to the list as archived orders.

### Shelf
Shelf is the basic data storage for the pickup area. Each shelf maintains it's own decay modifier.
There are normal overflow shelf and shelf with temperature, which can only store the order of the same temperature. 
Each shelf can only store the orders up to it's maximum capacity size.

### Pickup Area
Pickup Area is the main data structure that interacts with kitchen for the shelf management.
Each pickup area can hold one overshelf and multiple allowable shelves with the specific temperature.
Although it maintains two separate data store internally, the complexity is hidden and shelf/ order iterators are exposed for shelf policies.

### Order

Data class to store each individual order. The status, order age and inherent value ( deterioration value) will be changed during order life cycle.
The status can only be changed from one permitted state to another. There is the internal thread lock for concurrency control for each attribute. 
Currently, it's regular thread lock. But it should be replaced with read/write lock for better performance as further improvement.

### Shelf Policies

Shelf Policies are applied to each shelves through pickup are.
Those policies can be removed, changed order or replaced individually during run time. 
Currently, there are only four policies that
- calculate and update deterioration for each order
- discard spoiled orders
- discard random order if all shelves are full
- move order from one shelf to another
Additional policies can be implemented through ShelfPolicy interface.

### Courior


