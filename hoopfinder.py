#!/usr/bin/python
"""HOOP FINDER USING NYC BIGDATA XML"""
#http://www.nycgovparks.org/bigapps/DPR_Basketball_001.xml

import csv
from xml.etree import ElementTree as ET
import urllib2
import web
import  json

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

        #dataurl = "http://www.nycgovparks.org/bigapps/DPR_Basketball_001.xml"
        #xtext = urllib2.urlopen(dataurl).read()

        f= open('DPR_Basketball_001.xml', 'r')
        xtext=f.read()
    
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

        #make a json str
        hoopjson = json.dumps(facilities)
        #print hoopjson

        return render.hoopmap(**locals())
        
if __name__ == "__main__":
    app.run()
