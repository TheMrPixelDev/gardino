import datetime
import threading
import time

events = [[15, 1, 'on'],[30, 2, 'off']]

def trigger(time, id):
    print(f"Executing thread {id}")
    for _ in time:
        time.sleep(1)

threads = []

for event in events:
    thread = threading.Thread(function  =trigger, args=[event[0], event[1]])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

for _ in range(5):
    print("Waiting...")
    time.sleep(1)


