import sys
import os
import urllib2
from HTMLParser import HTMLParser
import textwrap

DOUBLE_NEWLINE_TAGS = ("h1", "h2", "p")
SINGLE_NEWLINE_TAGS = ("ul")
LINE_LENGTH = 120

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundDesc = False
        self.desc = ""
        self.isLink = False
        self.storedLink = ""
        self.isUnorderdList = False

    def get_link_from_tag(self, attrs):
        link = ""
        for at in attrs:
            if at[0] == "href":
                link = at[1]
                break
        return link

    def handle_tag(self, tag, attrs, isStart=True):
        if self.foundDesc:
            if tag == "em":
                self.desc += "_"
            elif tag == "a":
                if isStart:
                    self.storedLink = self.get_link_from_tag(attrs)
                else:
                    self.desc += "(" + self.storedLink + ")"
            elif tag == "li":
                if self.isUnorderdList:
                    if isStart:
                        self.desc += "\t - "
                if not isStart:
                    self.desc += "\n"



            if tag in DOUBLE_NEWLINE_TAGS and not isStart:
                self.desc += "\n\n"
            if tag in SINGLE_NEWLINE_TAGS and not isStart:
                self.desc += "\n"

    def handle_starttag(self, tag, attrs):
        for at in attrs:
            if at == ('class', 'day-desc'):
                self.foundDesc = True
        if tag == "a":
            self.isLink = True
        elif tag == "ul":
            self.isUnorderdList = True

        self.handle_tag(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag == "article" and self.foundDesc:
            self.foundDesc = False
        if tag == "a":
            self.isLink = False
        if tag == "ul":
            self.isUnorderdList = False
        self.handle_tag(tag, None, False)

    def handle_data(self, data):
        if self.isLink:
            data = "[" + data + "]"
        if self.foundDesc:
            self.desc += data

__dir__ = os.path.dirname(__file__)
DAY_NUM = int(os.path.basename(__dir__))
DAY_HTML_PATH = "http://adventofcode.com/2016/day/" + str(DAY_NUM)
DAY_HTML_INPUT_PATH = DAY_HTML_PATH + "/input"
DAY_HTML_DATA = urllib2.urlopen(DAY_HTML_PATH).read().replace("\n", "")

DAY_INPUT_PATH = os.path.join(__dir__, "input.txt")
DAY_INPUT = open(DAY_INPUT_PATH).readlines()

DAY_HTML_PARSER = MyHTMLParser()
DAY_HTML_PARSER.feed(DAY_HTML_DATA)
DAY_HTML_DESC = '\n'.join((textwrap.fill(x, LINE_LENGTH) for x in DAY_HTML_PARSER.desc.splitlines()))

print DAY_HTML_DESC
print "INPUT:\n{}".format(textwrap.fill(' '.join(DAY_INPUT), LINE_LENGTH))

# splitStr = [x.strip() for x in input.split(",")]
# L = complex(0, 1)
# R = complex(0, -1)
# dirs = [[(L if x[0] is "L" else R), int(x[1:])] for x in splitStr] # "into form [R, 1]..."
# z = complex(0, 0)
# for dir in reversed(dirs):
#         z = dir[0]*(dir[1] + z)
# z = L*z