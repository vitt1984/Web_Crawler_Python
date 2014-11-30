'''
Created on 30 november 2014

@author: Vittorio
'''

import os
from urllib.request import urlopen
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
           
    def handleQueueItem(self, queueItem, pagesQueue, pagesWithImage):
        """Receives the image from the parser and stores them in the shared dict
        """
        self.parser.reset()
        
        page = queueItem
            
        print ("Spider", os.getpid(), "Crawling page:", page)
        
        response = urlopen(page)
        data = response.read()
        text = data.decode()
        
        hostname = self.http + urlparse(page).hostname
        
        imageHRef = self.parser.feed(text, hostname)
        
        if imageHRef:
            pagesWithImage[page]=imageHRef
