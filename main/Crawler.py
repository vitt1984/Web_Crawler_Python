'''
Created on 22 juin 2013

@author: Vittorio
'''

import multiprocessing
from multiprocessing import Process
from collections import defaultdict

from main.spiders import PageSpider
from main.spiders import ImageSpider
import time
from urllib.parse import urlparse
import pprint
import operator
import math
            
if __name__ == "__main__":
    
    pp = pprint.PrettyPrinter(indent=4)
        
    m = multiprocessing.Manager()
    pagesQueue = m.Queue()
    visitedPages = m.dict()
    pagesWithImage = m.dict()
    processes = []

    startPage="http://www.ilfattoquotidiano.it/"
    words = ['renzi']
    
    print ("Assigning weight to words...")
    
    pagesQueue.put([startPage,0])
    
    weightedWords = defaultdict(int)
    for word in words:
        weightedWords[word.lower()] = math.pow(len(words)-words.index(word),2)
    
    pp.pprint(sorted(weightedWords.items(), key=operator.itemgetter(1)))
    
    print ("Creating spiders...")
    
    aPageSpider = PageSpider.PageSpider(weightedWords, 1, "http://" + urlparse(startPage).hostname)
    aImageSpider = ImageSpider.ImageSpider(weightedWords)
    
    print ("Sending spiders...")
    
    p1 = Process(target=aPageSpider.run, args=[pagesQueue,visitedPages])
    processes.append(p1)
    p1.start()
        
    time.sleep(10)
    
    for i in range(3):
        p = Process(target=aPageSpider.run, args=[pagesQueue,visitedPages])
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
    
    tenMostMatchingPages = sorted(visitedPages.items(), key=operator.itemgetter(1))[-10:]
    
    pp.pprint(tenMostMatchingPages)
    
    print ("For the ten closest matching pages, send a spider to check the most relevant images...")
    
    for pageWithWeight in tenMostMatchingPages:
        pagesQueue.put(pageWithWeight[0])

    aImageSpider.run(pagesQueue,pagesWithImage)

    pp.pprint(dict(pagesWithImage))

