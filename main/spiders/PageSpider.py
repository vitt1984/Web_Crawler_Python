'''
Created on 30 november 2014

@author: Vittorio
'''

import os

import urllib.request
from urllib.parse import urlparse

from main.parsers import PageSpiderParser
from main.spiders import Spider
                
class PageSpider (Spider.Spider):
    """PageSpider class
    Uses a PageSpiderParser to process queued items, returning:
        - the weight of the page
        - new links (if the distance from the initial page is not too high)
    The visited page is added to the shared dict with its weight for later stats
    """
    
    def __init__(self, weightedWords, maxDistance, hostnameFilter=None):
        super(PageSpider, self).__init__(weightedWords)
        self.parser = PageSpiderParser.PageSpiderParser(weightedWords)
        self.maxDistance = maxDistance
        self.hostnameFilter = hostnameFilter
            
    def handleQueueItem(self, queueItem, pagesQueue, visitedPages):
        """Receives the weight and new links from the parser:
        - the weight is stored in the shared dict along with the pages
        - the links are added if the distance is not too great
        """

        self.parser.reset()

        page = queueItem[0]
        distancePage = queueItem[1]
        
        if page not in visitedPages.keys():
            print ("Spider", os.getpid(), "(", distancePage ,"), Crawling page:", page)
            response = urllib.request.urlopen(page)
            data = response.read()
            text = data.decode()
            
            hostname = self.http + urlparse(page).hostname
            
            weight, hRefs = self.parser.feed(text, hostname, distancePage < self.maxDistance)
        
            for link in list(hRefs):
                linkHostname = self.http + urlparse(link).hostname
                
                if page != link and ((self.hostnameFilter is None) or (self.hostnameFilter == linkHostname)):
                    pagesQueue.put([link,distancePage+1])
                      
            visitedPages[page]=weight
                              
        else:
            print ("Spider", os.getpid(),  "(", distancePage ,") skipping page:", page)
            