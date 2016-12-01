import sys
import os
import re, time
import urllib2
from HTMLParser import HTMLParser
import textwrap
import cookielib
import shutil

__dir__ = os.path.dirname(__file__)

DOUBLE_NEWLINE_TAGS = ("h1", "h2", "p")
SINGLE_NEWLINE_TAGS = ("ul",)
LINE_LENGTH = 120

COOKIES_PATH = os.path.join(__dir__, "cookies.txt")
HTML_PATH_ROOT = "http://adventofcode.com"
DAY_HTML_DAY_PATH_BUILD = HTML_PATH_ROOT + "/{year}/day/{dayNum}"
DAY_HTML_DAY_PATH_INPUT_BUILD = DAY_HTML_DAY_PATH_BUILD + "/input"


class AdventHTMLParser(HTMLParser):
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


class AdventCookieJar(cookielib.FileCookieJar):
    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        now = time.time()
        try:
            while 1:
                line = f.readline()
                if line == "":
                    break

                # last field may be absent, so keep any trailing tab
                if line.endswith("\n"):
                    line = line[:-1]

                # skip comments and blank lines XXX what is $ for?
                if (line.strip().startswith(("#", "$")) or
                    line.strip() == ""):
                    continue

                domain, domain_specified, path, secure, expires, name, value = \
                        line.split("\t")
                secure = (secure == "TRUE")
                domain_specified = (domain_specified == "TRUE")
                if name == "":
                    # cookies.txt regards 'Set-Cookie: foo' as a cookie
                    # with no name, whereas cookielib regards it as a
                    # cookie with no value.
                    name = value
                    value = None

                initial_dot = domain.startswith(".")
                assert domain_specified == initial_dot

                discard = False
                if expires == "":
                    expires = None
                    discard = True

                # assume path_specified is false
                c = cookielib.Cookie(0, name, value,
                           None, False,
                           domain, domain_specified, initial_dot,
                           path, False,
                           secure,
                           expires,
                           discard,
                           None,
                           None,
                           {})
                if not ignore_discard and c.discard:
                    continue
                if not ignore_expires and c.is_expired(now):
                    continue
                self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            cookielib._warn_unhandled_exception()
            raise cookielib.LoadError("invalid Netscape format cookies file %r: %r" %
                            (filename, line))

    def save(self, filename=None, ignore_discard=False,
                 ignore_expires=False):
            if filename is None:
                if self.filename is not None:
                    filename = self.filename
                else:
                    raise ValueError(cookielib.MISSING_FILENAME_TEXT)

            f = open(filename, "w")
            try:
                now = time.time()
                for cookie in self:
                    if not ignore_discard and cookie.discard:
                        continue
                    if not ignore_expires and cookie.is_expired(now):
                        continue
                    if cookie.secure:
                        secure = "TRUE"
                    else:
                        secure = "FALSE"
                    if cookie.domain.startswith("."):
                        initial_dot = "TRUE"
                    else:
                        initial_dot = "FALSE"
                    if cookie.expires is not None:
                        expires = str(cookie.expires)
                    else:
                        expires = ""
                    if cookie.value is None:
                        # cookies.txt regards 'Set-Cookie: foo' as a cookie
                        # with no name, whereas cookielib regards it as a
                        # cookie with no value.
                        name = ""
                        value = cookie.name
                    else:
                        name = cookie.name
                        value = cookie.value
                    f.write(
                        "\t".join(
                            [cookie.domain, initial_dot, cookie.path,
                             secure, expires, name, value]) +
                        "\n")
            finally:
                f.close()


def getInputData(dayNum, year=2016):
    cj = AdventCookieJar("cookies.txt")
    cj.load()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    return opener.open(DAY_HTML_DAY_PATH_INPUT_BUILD.format(year=year, dayNum=dayNum)).read()


def getHtmlDesc(dayNum, year=2016):
    try:
        htmlData = urllib2.urlopen(DAY_HTML_DAY_PATH_BUILD.format(year=year, dayNum=dayNum)).read().replace("\n", "")
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "Page '{}' Not found".format(dayNum)
            return None
        else:
            raise e
    htmlParser = AdventHTMLParser()
    htmlParser.feed(htmlData)
    return htmlParser.desc


def prettyDesc(desc):
    return '\n'.join((textwrap.fill(x, LINE_LENGTH) for x in desc.splitlines()))


def prettyInput(inp):
    return textwrap.fill(inp, LINE_LENGTH)


def build(year=2016):
    for dayNum in range(1, 26):
        desc = getHtmlDesc(dayNum, year)
        if desc is None:
            break
        inpu = getInputData(dayNum, year)
        path = os.path.join(__dir__, "day", str(dayNum))
        descPath = os.path.join(path, "desc_"+str(dayNum)+".txt")
        inpuPath = os.path.join(path, "input_"+str(dayNum)+".txt")
        dayPyPath = os.path.join(path, "day_"+str(dayNum)+".py")
        with open(descPath, 'w') as descF, open(inpuPath, 'w') as inpuF:
            descF.write(prettyDesc(desc))
            inpuF.write(inpu)
            if not os.path.exists(dayPyPath):
                shutil.copyfile("day.py", dayPyPath)
            print "Page {} Found and info downloaded".format(dayNum)

if __name__ == "__main__":
    build()