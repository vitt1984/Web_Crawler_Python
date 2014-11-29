'''
Created on 22 juin 2013

@author: Vittorio
'''

import multiprocessing
from multiprocessing import Process
from collections import defaultdict

from main import Spider
import time
from urllib.parse import urlparse
import pprint
import operator
import math
            
if __name__ == "__main__":
    
    pp = pprint.PrettyPrinter(indent=4)
        
    #pool = multiprocessing.Pool(processes=4)
    m = multiprocessing.Manager()
    pagesQueue = m.Queue()
    
    # TODO not a set as it should be
    visitedPages = m.dict()
    
    #workers = pool.apply_async(aSpider.run(), pagesQueue)
    
    startPage="http://www.ilfattoquotidiano.it/"
    
    pagesQueue.put([startPage,0])
    
    words = ['berlusconi', 'ruby', 'processo']
    weightedWords = defaultdict(int)
    for word in words:
        weightedWords[word.lower()] = math.pow(len(words)-words.index(word),2)
    
    pp.pprint(sorted(weightedWords.items(), key=operator.itemgetter(1)))
    
    processes = []

    aSpider = Spider.Spider(weightedWords, 1, "http://" + urlparse(startPage).hostname)
    
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
        
    print ("All spiders back to nest. Removing pages with weight = 0...")
    
    for visitedPage in visitedPages.keys():
        if visitedPages[visitedPage] == 0:
            del visitedPages[visitedPage]
    
    print ("Ordering dict...")
    
    pp.pprint(sorted(visitedPages.items(), key=operator.itemgetter(1)))


