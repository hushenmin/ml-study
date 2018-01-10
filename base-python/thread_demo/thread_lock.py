import threading
def jobA():
    global  A,lock
    lock.acquire()
    for _ in range(100):
        A += 1
        print(str(A)+ " jobA")
    lock.release()
def jobB():
    lock.acquire()
    global  A,lock
    for _ in range(100):
        A += 10
        print(str(A)+" jobB")
    lock.release()
if __name__ == '__main__':
    lock = threading.Lock()
    A = 0;
    tA = threading.Thread(target=jobA(),)
    tB = threading.Thread(target=jobB(),)
    tA.start()
    tB.start()
    # tA.join()
    # tB.join()