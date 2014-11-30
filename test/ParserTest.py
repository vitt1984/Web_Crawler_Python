'''
Created on 30 november 2014

@author: Vittorio
'''

import unittest
from main.parsers import ImageSpiderParser, PageSpiderParser

class ParserTest(unittest.TestCase):
    """ Some basic unit test for the Parser
    The rest of the code is rather difficult to test
    """

    def setUp(self):
        self.weightedWords = {'test':9, 'bla':4, "oooh":1}
        self.hostname = "http://www.blabla.com"
        self.dataTextOnly = """<p>test oooh</p>"""
        self.dataTextOnly2 =  """<p>test<a href=\"http://www.blabla.com/test.html\">bla oooh</a>test<a href=\"http://www.blabla.com/test2.html\">bla test</a></p>"""
        self.dataTextWithImages = """<img data-src="http://www.blabla.com/test1.jpg" />"""
        self.dataTextWithImages2 = """<img data-src="http://www.blabla.com/test1.jpg" /><img data-src="http://www.blabla.com/test2oooh.png" />"""
    
    def testImageSpiderParser(self):
        imageSpiderParser = ImageSpiderParser.ImageSpiderParser(self.weightedWords)
        # check if it finds the image
        image = imageSpiderParser.feed(self.dataTextWithImages, self.hostname)
        self.assertTrue(image == "http://www.blabla.com/test1.jpg")
        # check that it chooses the image that matches the most
        image = imageSpiderParser.feed(self.dataTextWithImages2, self.hostname)
        print (image)
        self.assertTrue(image == "http://www.blabla.com/test2oooh.png")

    def testPageSpiderParser(self):
        pageSpiderParser = PageSpiderParser.PageSpiderParser(self.weightedWords)
        # check weight and that no links are retrieved
        weight, links = pageSpiderParser.feed(self.dataTextOnly, self.hostname, True)
        self.assertEqual(weight, 10)
        self.assertEqual(len(links),0)
        # check weight and that two links are retrieved if getNewLinks = True
        weight, links = pageSpiderParser.feed(self.dataTextOnly2, self.hostname, True)
        self.assertEqual(weight, 36)
        self.assertEqual(len(links),2)
        # check weight and that no links are retrieved if getNewLinks = False
        weight, links = pageSpiderParser.feed(self.dataTextOnly2, self.hostname, False)
        self.assertEqual(weight, 36)
        self.assertEqual(len(links),0)


if __name__ == '__main__':
    unittest.main()