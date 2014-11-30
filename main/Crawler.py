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
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Web Crawlers: return 10 most relevant pages and within these, the most relevant image.')
    parser.add_argument('-s', dest='startPage', action='store', required=True,
                       help='the first page that will be checked')
    parser.add_argument('-w', dest='words', nargs='+', required=True,
                       help='words to look for')
    parser.add_argument('--maxDepth', dest='maxDepth', type=int, default=1, required=False,
                       help='depth of link search. Default value is 1')
    parser.add_argument('--nbSpiders', dest='nbSpiders', type=int, default=3, required=False,
                       help='number of spiders that will be generated. Default value is 3')
    
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
        
    m = multiprocessing.Manager()
    pagesQueue = m.Queue()
    visitedPages = m.dict()
    pagesWithImage = m.dict()
    processes = []
    
    print ("Starting website: ", args.startPage)
    print ("Looking for words: ", args.words)
    print ("Max depth: ", args.maxDepth)
    print ("Number of spiders: ", args.nbSpiders)
    
    print ("Assigning weight to words...")
    
    pagesQueue.put([args.startPage,0])
    
    weightedWords = defaultdict(int)
    for word in args.words:
        weightedWords[word.lower()] = math.pow(len(args.words)-args.words.index(word),2)
    
    pp.pprint(sorted(weightedWords.items(), key=operator.itemgetter(1)))
    
    print ("Creating spiders...")
    
    aPageSpider = PageSpider.PageSpider(weightedWords, args.maxDepth, "http://" + urlparse(args.startPage).hostname)
    aImageSpider = ImageSpider.ImageSpider(weightedWords)
    
    print ("Sending spiders...")
    
    p1 = Process(target=aPageSpider.run, args=[pagesQueue,visitedPages])
    processes.append(p1)
    p1.start()
    
    # giving some time for the spider to fetch the first page and put some links inthe queue
    time.sleep(10)
    
    for i in range(args.nbSpiders):
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
    
    print ("Ordering visited pages...")
    
    tenMostMatchingPages = sorted(visitedPages.items(), key=operator.itemgetter(1))[-10:]
    
    pp.pprint(tenMostMatchingPages)
    
    print ("For the ten closest matching pages, send a spider to check the most relevant images...")
    
    for pageWithWeight in tenMostMatchingPages:
        pagesQueue.put(pageWithWeight[0])

    aImageSpider.run(pagesQueue,pagesWithImage)
    
    print ("Most relevant images:")

    pp.pprint(dict(pagesWithImage))

