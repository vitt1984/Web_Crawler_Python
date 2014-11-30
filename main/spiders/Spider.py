'''
Created on 30 november 2014

@author: Vittorio
'''

import sys
import os
import time
import datetime

import queue
                
class Spider:
    """Base Spider class
    Sub classes must implement the handleQueueItem method
    """
    
    http = "http://"
    
    def __init__(self, weightedWords):
        self.weightedWords = weightedWords
        
    def handleQueueItem(self, queueItem, pagesQueue, visitedPages):
        raise NotImplementedError("Subclasses should implement this!")
            
    def run(self, pagesQueue, visitedPages):
        """Run the process
        Get a page from the shared queue and process it
        """
        
        ts = time.time()
        print ("Spider", os.getpid(), "started crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        
        while not pagesQueue.empty():
            page = ""
            try:
                print ("Queue size:", pagesQueue.qsize() )
                print ("Visited pages size:", len(visitedPages))
                queueItem = pagesQueue.get(block=True, timeout=5)
                self.handleQueueItem(queueItem, pagesQueue, visitedPages)                
                sys.stdout.flush()
            except NotImplementedError as error:
                # the only blocking error
                raise error
            except queue.Empty:
                # this is in order to guarantee 
                break
            except Exception as error:
                # we should never stop the whole process because of an exception
                print (error,"with URL:",page)
                continue
          
        ts = time.time()  
        print ("Spider", os.getpid(), "stopped crawling at", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        

