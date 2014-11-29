'''
Created on 22 juin 2013

@author: Vittorio
'''

import multiprocessing
from multiprocessing import Process

from main import Spider
import time
            
if __name__ == "__main__":
    
    #pool = multiprocessing.Pool(processes=4)
    m = multiprocessing.Manager()
    pagesQueue = m.Queue()
    
    # TODO not a set as it should be
    visitedPages = m.list()

    aSpider = Spider.Spider()
    
    #workers = pool.apply_async(aSpider.run(), pagesQueue)
    
    pagesQueue.put(["http://en.wikipedia.org/wiki/Italy",0])
        
    processes = []
    
    p1 = Process(target=aSpider.run, args=[pagesQueue,visitedPages])
    processes.append(p1)
    p1.start()
        
    time.sleep(10)
    
    for i in range(3):
        p = Process(target=aSpider.run, args=[pagesQueue,visitedPages])
        processes.append(p)
        p.start()
        
    print ("Waiting for the spiders to come back...")
    
    for p in processes:
        p.join()
        
    print ("All spiders back to nest...")


