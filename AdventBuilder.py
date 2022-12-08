"""
Be careful when using this! The site can't take a lot of people accessing it at once and so all web
requests are with a delay of 5 seconds to stop a DDOS of the site. I recommend you skip the days you
have already downloaded in the build function and use sparingly!
"""
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError

import os
import time
import datetime
import argparse

from html.parser import HTMLParser
    

from http.cookiejar import FileCookieJar, MozillaCookieJar, _warn_unhandled_exception, LoadError
from http.cookies import SimpleCookie as Cookie
    
    
import textwrap

import shutil


__dir__ = os.path.dirname(__file__)

SINGLE_NEWLINE_TAGS = ("h1", "h2", "p")
LINE_LENGTH = 120
START_YEAR = 2015
NOW = datetime.datetime.now()
SKIP_DEFAULT = set(range(1, NOW.day)) if NOW.month >= 12 else set()
VALID_YEARS = tuple(START_YEAR+i for i in range(NOW.year + (NOW.month >= 12) - START_YEAR))

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
        self.isCode = False
        self.isPre = False

    @staticmethod
    def get_link_from_tag(attrs):
        link = ""
        for at in attrs:
            if at[0] == "href":
                link = at[1]
                break
        return link

    def handle_tag(self, tag, attrs, isStart=True):
        if self.foundDesc:
            if tag == "em":
                if self.isPre or self.isCode:
                    self.desc += "<b>" if isStart else "</b>"
                else:
                    self.desc += "__"
            elif tag == "a":
                if isStart:
                    self.storedLink = self.get_link_from_tag(attrs)
                else:
                    self.desc += "(" + self.storedLink + ")"
            elif tag == "li":
                if self.isUnorderdList:
                    if isStart:
                        self.desc += "- "
                if not isStart:
                    self.desc += "\n"
            elif tag == "code":
                if self.isPre:
                    self.desc += "<pre>" if isStart else "</pre>"
                    self.desc += "\n"
                else:
                    self.desc += "<code>" if isStart else "</code>"
            elif tag == "h2" and isStart:
                self.desc += "# "

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
        elif tag == "code":
            self.isCode = True
        elif tag == "pre":
            self.isPre = True

        self.handle_tag(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag == "article" and self.foundDesc:
            self.foundDesc = False
        elif tag == "a":
            self.isLink = False
        elif tag == "ul":
            self.isUnorderdList = False
        elif tag == "code":
            self.isCode = False
        elif tag == "pre":
            self.isPre = False

        self.handle_tag(tag, None, False)

    def handle_data(self, data):
        if self.isLink:
            data = "[" + data + "]"
        if self.isUnorderdList:
            data = data.strip("\n")
        if self.foundDesc:
            self.desc += data


class AdventCookieJar(FileCookieJar):
    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        now = time.time()
        line = None
        try:
            while 1:
                line = f.readline()
                if line == "":
                    break

                # last field may be absent, so keep any trailing tab
                if line.endswith("\n"):
                    line = line[:-1]

                # skip comments and blank lines XXX what is $ for?
                if line.strip().startswith(("#", "$")) or line.strip() == "":
                    continue

                # assume path_specified is false
                c = Cookie(line)
                self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            _warn_unhandled_exception()
            raise LoadError("invalid Netscape format cookies file %r: %r" %
                                      (filename, line))

    def save(self, filename=None, ignore_discard=False,
             ignore_expires=True):
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


def createHtmlLoader():
    cj = MozillaCookieJar("cookies.txt")
    cj.load()
    opener = build_opener(HTTPCookieProcessor(cj))
    return opener


def getInputData(dayNum, year=2016, opener=None, delay=5, firstTime=True):
    return getHtmlPageWithCookies(DAY_HTML_DAY_PATH_INPUT_BUILD.format(year=year, dayNum=dayNum), opener, delay, firstTime).decode("utf-8")


def getHtmlPageWithCookies(path, opener=None, delay=5, firstTime=True):
    if not firstTime:
        time.sleep(delay)

    if opener is None:
        opener = createHtmlLoader()
    try:
        html = opener.open(path).read()
    except HTTPError as e:
        if e.code == 404:
            print("Page '{}' Not found".format(path))
            return None
        else:
            raise e
    return html


def getHtmlDesc(dayNum, year=2016, opener=None, delay=5, firstTime=True):
    html = getHtmlPageWithCookies(DAY_HTML_DAY_PATH_BUILD.format(year=year, dayNum=dayNum), opener, delay, firstTime)
    if html is None:
        return None
    else:
        pass

    htmlParser = AdventHTMLParser()
    htmlParser.feed(html.decode("utf-8") )
    return htmlParser.desc


def prettyDesc(desc):
    return '\n'.join((textwrap.fill(x, LINE_LENGTH) for x in desc.splitlines()))


def prettyInput(inp):
    return '\n'.join([textwrap.fill(x, LINE_LENGTH) for x in inp.splitlines()][:5]) + "\n..."


def prettyInfo(desc, inp):
    return '\n'.join((prettyDesc(desc), "\nINPUT:", prettyInput(inp), "\n"))


def prettyAnswers(task1, task2):
    return '\n'.join(("--- ANSWERS ---", "Task 1: " + str(task1), "Task 2: " + str(task2)))


def setupDayVariables(path):
    try:
        baseDir = os.path.basename(path)
        DAY_NUM = int(baseDir.split("day")[1])
        DAY_DESC = ''.join(open(os.path.join(path, "desc_{}.md".format(DAY_NUM))).readlines())
        DAY_INPUT = open(os.path.join(path, "input_{}.txt".format(DAY_NUM))).read().splitlines()
        DAY_INPUT_STR = '\n'.join(DAY_INPUT)
    except ValueError:
        print("File {} in advent day folder".format(path))
        DAY_NUM = 0
        DAY_DESC = ""
        DAY_INPUT = ""
        DAY_INPUT_STR = ""

    return DAY_NUM, DAY_DESC, DAY_INPUT, DAY_INPUT_STR


def build(year=(2015,), overwriteSolution=False, overwriteDesc=False, overwriteInput=False, overwriteDayPy=False, overwriteParentInit=False, delay=5, noskip=False, skip=set()):
    opener = createHtmlLoader()
    firstTime = True
    if noskip:
        skip = set()

    for y in year:
        christmas_date = datetime.date(year=y, month=12, day=25)
        end_range = christmas_date.day + 1 if datetime.datetime.now().date() > christmas_date else datetime.datetime.now().day + 1

        dayParent = os.path.join(__dir__, str(y), "day")
        parentInit = os.path.join(dayParent, "__init__.py")
        if not os.path.exists(parentInit) or overwriteParentInit:
            if not os.path.exists(dayParent):
                os.makedirs(dayParent)

            print(f"Writing {parentInit}")
            with open(parentInit, 'w+') as initF:
                initF.write('"""day init"""')

        for dayNum in range(1, end_range):
            if dayNum in skip:
                print("Skipping dayNum {}".format(dayNum))
                continue

            dayPath = os.path.join(dayParent, "day"+str(dayNum))

            if os.path.exists(dayPath) and not any((overwriteDesc, overwriteInput, overwriteDayPy, overwriteSolution, overwriteParentInit)):
                print("Not overwriting and files already downloaded: {}".format(dayNum))
                continue
            else:
                pathExists = True

            pyFileName = "day_" + str(dayNum)

            descPath = os.path.join(dayPath, "desc_" + str(dayNum) + ".md")
            inpuPath = os.path.join(dayPath, "input_" + str(dayNum) + ".txt")
            dayPyPath = os.path.join(dayPath, pyFileName + ".py")
            initPath = os.path.join(dayPath, "__init__.py")
            filesCreated = False


            if not os.path.exists(descPath) or overwriteDesc:
                desc = getHtmlDesc(dayNum, y, opener, delay, firstTime)
                firstTime = False
                if desc is None:
                    break
                else:
                    print("Page {} found".format(dayNum))

            if not os.path.exists(inpuPath) or overwriteInput:
                inpu = getInputData(dayNum, y, opener, delay, firstTime)
                firstTime = False

            if not os.path.exists(dayPyPath) or overwriteDayPy:
                if not os.path.exists(os.path.dirname(dayPyPath)):
                    os.makedirs(os.path.dirname(dayPyPath))
                shutil.copyfile("day.py", dayPyPath)
                print("\tday.py copied to {}".format(dayPyPath))
                filesCreated = True

            if not os.path.exists(descPath) or overwriteDesc:
                with open(descPath, 'w+') as descF:
                    descF.write(prettyDesc(desc))
                print("\tDescription created at {}".format(descPath))
                filesCreated = True

            if not os.path.exists(inpuPath) or overwriteInput:
                with open(inpuPath, 'w+') as inpuF:
                    inpuF.write(inpu)
                print("\tInput created at {}".format(descPath))
                filesCreated = True

            if not os.path.exists(initPath) or overwriteSolution:
                with open(initPath, 'w+') as initF:
                    initF.write("from {} import *".format(pyFileName))
                filesCreated = True

            if not filesCreated:
                print("\t No files created")


class ParseRange(argparse.Action):
    """Parses argparse argument as a range"""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) >= 0:
            setattr(namespace, self.dest, set())

        if isinstance(values, str):
            values = (values,)

        for v in values:
            if v.startswith("r"):
                setattr(namespace, self.dest, getattr(namespace, self.dest).union(set(range(*(int(x) for x in v[1:].split(":"))))))
            else:
                getattr(namespace, self.dest).add(int(v))




def argparser():
    ag = argparse.ArgumentParser(description="Download advent of code for offline use and help setup code")
    ag.add_argument("year", type=int, help="the year", nargs="+", choices=VALID_YEARS, default=NOW.year)
    ag.add_argument("--overwriteSolution", "-o", action="store_true", help="whether we can overwrite the solution")
    ag.add_argument("--overwriteDayPy", "-odp", action="store_true", help="whether we can overwrite the day python file")
    ag.add_argument("--overwriteDesc", "-od", action="store_true", help="whether we should overwrite the description")
    ag.add_argument("--overwriteInput", "-oi", action="store_true", help="whether we should overwrite the input")
    ag.add_argument("--overwriteParentInit", "-opi", action="store_true", help="whether we should overwrite the parent init")
    ag.add_argument("--delay", "-d", type=int, help="how long the delay", default=5)
    ag.add_argument("--skip", "-s", action=ParseRange, type=str, nargs="*", default=tuple(),
                    help="what days to skip as either numbers in a list or range format by prefixing with 'r'")
    ag.add_argument("--noskip", "-ns", action="store_true", help="to disable any skipping. Same as putting --skip and leaving blank")
    return ag


if __name__ == "__main__":
    agp = argparser()
    args = agp.parse_args()
    build(**args.__dict__)
