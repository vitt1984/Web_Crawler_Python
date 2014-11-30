'''
Created on 30 november 2014

@author: Vittorio
'''

import os
import re

from main.parsers import SpiderParser

class ImageSpiderParser(SpiderParser.SpiderParser):
    """ImageSpiderParser class
    Returns the most relevant image in the page, based on the search words
    """
    
    imagesAttributes = ['data-src','src']
    relevantPages = re.compile('(jpg|png|gif)$')
    
    def __init__(self, weightedWords, strict=False):
        SpiderParser.SpiderParser.__init__(self, weightedWords, strict=strict)
        self.relevantAttributes = self.imagesAttributes
                
    def feed(self, data, hostname):
        """Examines the images and chooses the one with the highest weight
        """
        super(ImageSpiderParser, self).feed(data, hostname)
        
        heaviestHref = None # by default we return nothing
        hRefMaxWeight = 0

        for hRef in self.links:
            if self.relevantPages.search(hRef):
                hRefWeight = 0
                for word in self.weightedWords.keys():
                    if word in hRef:
                        print ("Spider", os.getpid(), "found", word, "adding",self.weightedWords[word.lower()],"to this image")
                        hRefWeight += self.weightedWords[word]
                if hRefWeight > hRefMaxWeight:
                    hRefMaxWeight = hRefWeight
                    heaviestHref = hRef
        
        return heaviestHref
            