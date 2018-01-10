import  multiprocessing as mp
def job(a):
    return  a * a

def multicore():
    pool = mp.Pool()
    res = pool.map(job,xrange(100))
    print res
if __name__ == '__main__':
    multicore()
