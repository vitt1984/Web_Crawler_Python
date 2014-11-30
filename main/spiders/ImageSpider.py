'''
Created on 22 juin 2013

@author: Vittorio
'''
import os
import urllib.request
from urllib.parse import urlparse

from main.parsers import ImageSpiderParser
from main.spiders import Spider
        
class ImageSpider(Spider.Spider):
    """ImageSpider class
    Checks all the images in the page, and finds out which one is the most relevant to the searched words
    """
    
    def __init__(self, weightedWords):
        super(ImageSpider, self).__init__(weightedWords)
        self.parser = ImageSpiderParser.ImageSpiderParser(weightedWords)
           
    def handleQueueItem(self, queueItem, pagesQueue, visitedPages):
        """Receives the image from the parser and stores them in the shared dict
        """
        self.parser.reset()
        
        page = queueItem
            
        print ("Spider", os.getpid(), "Crawling page:", page)
        
        response = urllib.request.urlopen(page)
        data = response.read()
        text = data.decode()
        
        hostname = "http://" + urlparse(page).hostname
        
        imageHRef = self.parser.feed(text, hostname)
        
        if imageHRef:
            visitedPages[page]=imageHRef
