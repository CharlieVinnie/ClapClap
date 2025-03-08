import threading
import time

condition = threading.Condition()
shared_data_ready = False

def worker(thread_id):
    global shared_data_ready
    with condition:  # Locking the condition before calling wait()
        while not shared_data_ready:
            print(f"Thread {thread_id} is waiting...")
            condition.wait()  # This releases the lock and waits
        print(f"Thread {thread_id} resumed work!")

def notifier():
    global shared_data_ready
    time.sleep(2)  # Simulate work
    with condition:  # Locking the condition before calling notify_all()
        shared_data_ready = True
        print("Notifying all threads!")
        condition.notify_all()  # Wake up all waiting threads

# Start worker threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()

# Start notifier thread
notifier_thread = threading.Thread(target=notifier)
notifier_thread.start()

# Wait for all threads to finish
for t in threads:
    t.join()
notifier_thread.join()
