from bs4 import BeautifulSoup
import re

r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify_2space(s, encoding=None, formatter="minimal"):
    return r.sub(r'\1\1', s.prettify(encoding, formatter))

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

def prettify(html):
    soup = BeautifulSoup(html)
    return soup.prettify(indent_width=4)

