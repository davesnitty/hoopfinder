#!/usr/bin/python
"""HOOP FINDER USING NYC BIGDATA XML"""
#http://www.nycgovparks.org/bigapps/DPR_Basketball_001.xml

import csv
from xml.etree import ElementTree as ET
import urllib2
import web
import  json
import hashlib
import sys

from web.contrib.template import render_cheetah

render = render_cheetah('templates/')
        
urls = (
    r'/hoopmap/', 'Hoopmap'
)
app = web.application(urls, globals())

class Hoopmap:
    def GET(self):
        print "Hoop Finder"

        facilities = []
        

        f= open('DPR_Basketball_001.xml', 'r')
        xtext=f.read()
        xtext = xtext.replace('&','&amp;')        

        xtree = ET.XML(xtext)

        for x in xtree:
            for y in x:
                childs= y.getchildren()
                facility = {}
                for c in childs:
                    #print c.tag.split('}',1)[1], ' ', web.safestr(c.text)
                    facility[c.tag.split('}',1)[1]] = web.safestr(c.text)
                facilities.append(facility)
        
        #print facilities[0:3]

        #print len(facilities)

        #make a json str
        hoopjson = json.dumps(facilities)
        #print hoopjson

        return render.hoopmap(**locals())
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'update':
            sys.argv[1] = '' #reset argument to avoid conflicts with wsgi server
            dataurl = "http://www.nycgovparks.org/bigapps/DPR_Basketball_001.xml"
            newfile_text = urllib2.urlopen(dataurl).read()

            f= open('DPR_Basketball_001.xml', 'r')
            existfile_text = f.read()

            newhash = hashlib.sha1(newfile_text).hexdigest()
            existhash = hashlib.sha1(existfile_text).hexdigest()

            print 'new= ' + newhash
            print 'old= ' + existhash

            if newhash != existhash:
                print 'updating file'
                f.close()
                f= open('DPR_Basketball_001.xml', 'w')
                f.write(newfile_text)
                f.close()
                print 'file updated'
            else:
                print 'files identical - no need to update'
    
    app.run()
