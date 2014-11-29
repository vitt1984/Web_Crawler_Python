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
    global weight
    global weightedWords
    global hostname
            
    def handle_starttag(self, tag, attrs):
        #print("Start tag  :", tag)
        self.currentTags.append(tag)
        for attr in attrs:
            if attr[0] == "href" and not (attr[1].startswith("#") or attr[1].startswith("javascript")) and not (attr[1].endswith(".css") or attr[1].endswith(".rss") or attr[1].endswith(".js")):
                link = attr[1]
                if link.startswith("//"):
                    link = "http:" + link                    
                elif link.startswith("/"):
                    link = self.hostname + link
                if link.startswith("http"):
                    self.hRefs.add(link)
            
    def handle_endtag(self, tag):
        del self.currentTags[-1]
        #print("End tag  :", tag)
        
    def handle_data(self, data):
        if (len(self.currentTags) > 0 and self.currentTags[-1] in ['a','p']):            
            for word in re.compile('\w{3}\w+').findall(data):
                if (word.lower() in self.weightedWords.keys()):
                    print ("Spider", os.getpid(), "found", word, "adding",self.weightedWords[word.lower()])
                    self.weight += self.weightedWords[word.lower()]
                
    def feed(self, data, hostname, weightedWords):
        self.currentTags = []
        self.hRefs = set()
        self.weight = 0
        self.weightedWords = weightedWords
        self.hostname = hostname
        super(SpiderParser, self).feed(data)
        return self.weight, self.hRefs
            