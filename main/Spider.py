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

class SpiderParser(HTMLParser):
    
    global currentTags
    global hRefs
    global countedWords
    global websiteRoot
            
    def handle_starttag(self, tag, attrs):
        #print("Start tag  :", tag)
        self.currentTags.append(tag)
        for attr in attrs:
            if 'href' == attr[0] and not (attr[1].startswith("#") or attr[1].startswith("javascript")):
                link = attr[1]
                if link.startswith("//"):
                    link = "http:" + link                    
                elif link.startswith("/"):
                    link = self.hostname + link
                self.hRefs.add(link)
            
    def handle_endtag(self, tag):
        del self.currentTags[-1]
        #print("End tag  :", tag)
        
    def handle_data(self, data):
        if (len(self.currentTags) > 0 and self.currentTags[-1] in ['a','p']):
            #print("Tag: ", self.currentTags[-1], ", Data     :", data.encode('utf-8'))
            
            for word in re.compile('\w{3}\w+').findall(data):
                self.countedWords[word.lower()] += 1
                
    def feed(self, data, hostname):
        self.currentTags = []
        self.hRefs = set()
        self.countedWords = Counter()
        self.hostname = hostname
        super(SpiderParser, self).feed(data)
        return self.countedWords.most_common(50), self.hRefs
            
                
class Spider:
    
    global parser
    
    def __init__(self):
        self.parser = SpiderParser()     
            
    def run(self, pagesQueue, visitedPages):
        r"""Run the process
        
        Get a page from the shared queue and process it
        """
        
        ts = time.time()
        print ("Spider ", os.getpid(), " started crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            
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
                print ("Visited pages size:", len(visitedPages) )
                pageAndDistance = pagesQueue.get(block=True, timeout=5)
                page = pageAndDistance[0]
                distancePage = pageAndDistance[1]
                
                if page not in visitedPages:
                    visitedPages.append(page)
                    print ("Spider", os.getpid(), ", Crawling page:", page)
                    response = urllib.request.urlopen(page)
                    data = response.read()      # a `bytes` object
                    text = data.decode() # a `str`; this step can't be used if data is binary
                    
                    hostname = "http://" + urlparse(page).hostname
                    
                    countedWords, hRefs = self.parser.feed(text, hostname)
                    
                    pp = pprint.PrettyPrinter(indent=4)
                    
                    #pp.pprint(countedWords)
                    #pp.pprint(hRefs)
                    
                    if distancePage <= 3:
                        pp.pprint(list(hRefs)[0:4])
                        for link in list(hRefs)[0:4]:
                            if not page == link:
                                pagesQueue.put([link,distancePage+1])
                    
                    sys.stdout.flush()
                
            except queue.Empty:
                break
            except UnicodeDecodeError as error:
                print (error,"with URL:",page)
                continue
            except urllib.error.URLError as error:
                print (error,"with URL:",page)
                continue
          
        ts = time.time()  
        print ("Spider", os.getpid(), "stopped crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        

