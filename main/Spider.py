'''
Created on 22 juin 2013

@author: Vittorio
'''

import urllib.request

import re

import sys
import codecs
from html.parser import HTMLParser
from html.entities import name2codepoint
from test.test_descrtut import defaultdict
from collections import Counter
import pprint
import os
import time
import datetime
from urllib.parse import urlparse

import queue
from multiprocessing import Queue
from main import SpiderParser
                
class Spider:
    
    global parser
    global maxDistance
    global weightedWords
    global hostnameFilter
    
    def __init__(self, weightedWords, maxDistance, hostnameFilter=None):
        self.parser = SpiderParser.SpiderParser()
        self.weightedWords = weightedWords
        self.maxDistance = maxDistance
        self.hostnameFilter = hostnameFilter
            
    def run(self, pagesQueue, visitedPages):
        r"""Run the process
        
        Get a page from the shared queue and process it
        """
        
        ts = time.time()
        print ("Spider", os.getpid(), "started crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            
        #htmlTextRE = re.compile("<a.*>(.*)</a>")
        #textRE = re.compile("<p>(.*)</p>")
        #sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        
        while not pagesQueue.empty():
            page = ""
            hRefs = []
            self.parser.reset()
            text = None
            data = None
            response = None
            try:
                print ("Queue size:", pagesQueue.qsize() )
                print ("Visited pages size:", len(visitedPages.keys()) )
                pageAndDistance = pagesQueue.get(block=True, timeout=5)
                page = pageAndDistance[0]
                distancePage = pageAndDistance[1]
                
                if page not in visitedPages.keys():
                    print ("Spider", os.getpid(), "(", distancePage ,"), Crawling page:", page)
                    response = urllib.request.urlopen(page)
                    data = response.read()      # a `bytes` object
                    text = data.decode() # a `str`; this step can't be used if data is binary
                    
                    hostname = "http://" + urlparse(page).hostname
                    
                    weight, hRefs = self.parser.feed(text, hostname, self.weightedWords)
                    
                    #self.pp.pprint(countedWords)
                    #self.pp.pprint(hRefs)
                    
                    if distancePage <= self.maxDistance:
                        for link in list(hRefs):
                            linkHostname = "http://" + urlparse(link).hostname
                            #print (self.hostnameFilter, linkHostname, (self.hostnameFilter == linkHostname))
                            #print ("Spider", os.getpid(), self.hostnameFilter, link, (page != link and ((self.hostnameFilter is None) or (self.hostnameFilter == linkHostname))), "from", page)
                            
                            if page != link and ((self.hostnameFilter is None) or (self.hostnameFilter == linkHostname)):
                                pagesQueue.put([link,distancePage+1])
                              
                    visitedPages[page]=weight
                                      
                else:
                    print ("Spider", os.getpid(),  "(", distancePage ,") skipping page:", page)

                sys.stdout.flush()
            except queue.Empty:
                break
            except Exception as error:
                print (error,"with URL:",page)
                continue
          
        ts = time.time()  
        print ("Spider", os.getpid(), "stopped crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        

