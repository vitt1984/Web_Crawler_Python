'''
Created on 30 november 2014

@author: Vittorio
'''

import re

import os
from main.parsers import SpiderParser

class PageSpiderParser(SpiderParser.SpiderParser):
    """PageSpiderParser class
    Returns:
        - weight of the page
        - links contained in the page
    """
    
    hrefAttributes = ['href']
    relevantTags = ['a','p']
    relevantWordsRE = re.compile('\w+')
    
    def __init__(self, weightedWords, strict=False):
        SpiderParser.SpiderParser.__init__(self, weightedWords, strict=strict)

    def handle_data(self, data):
        """Sets the new weight based on the content of the data
        """
        if (len(self.currentTags) > 0 and self.currentTags[-1] in self.relevantTags):            
            for word in self.relevantWordsRE.findall(data):
                if (word.lower() in self.weightedWords.keys()):
                    print ("Spider", os.getpid(), "found", word, "adding",self.weightedWords[word.lower()])
                    self.weight += self.weightedWords[word.lower()]
                
    def feed(self, data, hostname, getNewLinks):
        """Note: only fetches 'hrefs' attributes if new links are needed
        """
        self.weight = 0
        if getNewLinks:
            self.relevantAttributes = self.hrefAttributes
        else:
            self.relevantAttributes = []
        super(PageSpiderParser, self).feed(data, hostname)
        return self.weight, self.links
            