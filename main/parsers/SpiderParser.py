'''
Created on 30 november 2014

@author: Vittorio
'''

import re

from html.parser import HTMLParser
from urllib.parse import urljoin

class SpiderParser(HTMLParser):
    """SpiderParser class
    Overrides HTMLParser
    Basic tag handling and attributes harvesting.
    The subclass has to specify the necessary attributes.
    """
    
    unwantedFiles= set([".css",".rss",".js"]) # list might be longer...
    fileExtensionRe=re.compile("\.[a-zA-Z0-9]+$")
        
    def __init__(self, weightedWords, strict=False):
        HTMLParser.__init__(self, strict=strict)
        self.weightedWords = weightedWords
            
    def handle_starttag(self, tag, attrs):
        self.currentTags.append(tag)
        for attr in attrs:
            fileExtension = self.fileExtensionRe.search(attr[1])
            if attr[0] in self.relevantAttributes and (fileExtension is None or fileExtension not in self.unwantedFiles):
                link = attr[1]
                if link.startswith("/"):
                    link = urljoin(self.hostname, link)
                if link.startswith("http"):
                    self.links.add(link)
            
    def handle_endtag(self, tag):
        del self.currentTags[-1]
                
    def feed(self, data, hostname):
        """PageSpiderParser class
        Examines the images and chooses the one with the highest weight
        """
        if self.relevantAttributes is None:
            raise NotImplementedError("Relevant attributes not specified by sub class")

        self.currentTags = []
        self.links = set()
        self.hostname = hostname
        super(SpiderParser, self).feed(data)
            