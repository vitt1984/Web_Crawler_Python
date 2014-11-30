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
    """SpiderParser class
    Basic tag handling and attributes harvesting.
    The subclass has to specify the necessary attributes.
    """
    
    global currentTags
    global hRefs
    global hostname
    global weightedWords
    global relevantAttributes
    
    def __init__(self, weightedWords, strict=False):
        HTMLParser.__init__(self, strict=strict)
        self.weightedWords = weightedWords
            
    def handle_starttag(self, tag, attrs):
        self.currentTags.append(tag)
        for attr in attrs:
            if attr[0] in self.relevantAttributes and not (attr[1].startswith("#") or attr[1].startswith("javascript")) and not (attr[1].endswith(".css") or attr[1].endswith(".rss") or attr[1].endswith(".js")):
                link = attr[1]
                if link.startswith("//"):
                    link = "http:" + link                    
                elif link.startswith("/"):
                    link = self.hostname + link
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
            