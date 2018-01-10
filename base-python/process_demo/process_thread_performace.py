import  threading as td
import  multiprocessing as mp
import time
import Queue
def job(q):
    res = 0
    for i in range(100000000):
        res =i + i**2 + i**3
    q.put(res)
def normal():
    res = 0
    for j in range(2):
        for i in range(100000000):
            res =i + i**2 + i**3
            return str(res) + " normal"
def multi_core():
    q = mp.Queue()
    p1 = mp.Process(target=job,args=(q,))
    p2 = mp.Process(target=job,args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    return str(q.get()+q.get())+" multicore"
def multi_threads():
    q = Queue.Queue()
    t1 = td.Thread(target=job,args=(q,))
    t2 = td.Thread(target=job,args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return str(q.get() + q.get()) + " multi_threads"
if __name__ == '__main__':
   t_n = time.time()
   normal()
   print time.time()-t_n
   t_m = time.time()
   multi_threads()
   print time.time() - t_m
   t_th = time.time()
   print time.time()-t_th





