import multiprocessing as mp
def job(q):
    res = 0
    for i in range(1000):
        res += i;
    q.put(res)
if __name__ == '__main__':
    q = mp.Queue()
    p1 = mp.Process(target=job,args=(q,))
    p2 = mp.Process(target=job,args=(q,))
    p1.start()
    p2.start()
    # p1.join()
    # p2.join()
    print q.get()
    print q.get()

    # print q.get()+q.get()
