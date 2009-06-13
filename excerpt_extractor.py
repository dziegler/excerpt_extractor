"""
This is a simple script to automatically extract excerpts from articles. It
requires BeautifulSoup.

Usage:
from excerpt_extractor import get_summary
url = "http://someurl.com/goes/here"
(title,description) = get_summary(url)

==========================================

Some examples, discussion, and comparison with the Facebook article extractor
are at http://blog.davidziegler.net/post/122176962/a-python-script-to-automatically-extract-excerpts-from

copyright: Copyright 2009 by David Ziegler
license: MIT License
website: http://github.com/dziegler/excerpt_extractor/tree/master 
"""
from BeautifulSoup import *
import urllib2
import cookielib
import re

def cleanSoup(soup):
    # get rid of javascript, noscript and css
    for elem in ('script','noscript','style'):
        subtree = soup(elem)
        [tree.extract() for tree in subtree]
    # get rid of doctype
    subtree = soup.findAll(text=re.compile("DOCTYPE"))
    [tree.extract() for tree in subtree]
    # get rid of comments
    comments = soup.findAll(text=lambda text:isinstance(text,Comment))
    [comment.extract() for comment in comments]
    return soup

def removeHeaders(soup):
    for header in ('h1','h2','h3','h4','h5','h6'):
        subtree = soup(header)
        [tree.extract() for tree in subtree]
    return soup

def get_summary(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    doc = opener.open(url).read()
    soup = cleanSoup(BeautifulSoup(doc,parseOnlyThese=SoupStrainer('head')))
    
    if not soup:
      raise ValueError, "Invalid output: %s" % url
    
    try:
        title = soup.head.title.string
    except:
        title = None
    
    description = ''
    for meta in soup.findAll('meta'):
        if 'description' == meta.get('name', '').lower():
            description = meta['content']
            break
        
    if not description:
        soup = removeHeaders(cleanSoup(BeautifulSoup(doc,parseOnlyThese=SoupStrainer('body'))))
        text = ''.join(soup.findAll(text=True)).split('\n')
        description = max((len(i.strip()),i) for i in text)[1].strip()[0:255]

    return (title, description)

if __name__ == "__main__":
    urllist=("http://www.sfgate.com/cgi-bin/article.cgi?f=/c/a/2009/06/04/DD7V1806SV.DTL&type=performance",
              "http://www.chloeveltman.com/blog/2009/05/two-very-different-symphonies.html#links",
              "http://www.chloeveltman.com/blog/2009/06/child-prodigy-at-peabody-essex-museum.html#links",
              "http://www.sfgate.com/cgi-bin/article.cgi?f=/c/a/2009/06/04/NS9617O7JK.DTL&type=performance",
              "http://blogs.mercurynews.com/aei/2009/06/04/ramya-auroprem-joins-cast-of-spelling-bee/",
              "http://www.mercurynews.com/karendsouza/ci_12510394",
              "http://www.reason.com/news/show/134059.html")
    for u in urllist:
        print get_summary(u)[1] + '\n'
    
