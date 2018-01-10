import multiprocessing as mp
import  threading as td
def job(a,b):
    print a+b
if __name__ =="__main__":
    t = td.Thread(target=job(4, 2), )
    p = mp.Process(target=job(4, 3), )
    t.start()
    p.start()
    t.join()
    p.join()