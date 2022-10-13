import threading
import time

event1 = threading.Event()
event2 = threading.Event()
events = [event1,event2]

def myfunction1(event):
    while True:
        event.wait()
        # do stuff
        print("do stuff 1")
        event.clear()

def myfunction2(event):
    while True:
        event.wait()
        # do stuff
        print("do stuff 2")
        event.clear()

def tick_events(events):
    while True:
        time.sleep(1)
        for event in events:
            event.set()
        print("all thread sets")

t1 = threading.Thread(target=myfunction1, args=(event1,)).start()
t2 = threading.Thread(target=myfunction2, args=(event2,)).start()
t3 = threading.Thread(target=tick_events, args=(events,)).start()




