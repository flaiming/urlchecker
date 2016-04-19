import re
from urlparse import urlparse
import requests


PARKED_PHRASES = (
    r'godaddy\.com/park',
    r'(?:domain|website)\s+(?:name)?\s*(?:is)?\s*for\s+sale',
    r'buy\s+this\s+domain',
    r'sedoparking\.com',
    r'registrar_frameset',
    r'domain\s+has\s+expired',
    r'domain\s+(?:is)?\s*\s*parked',
)
MIN_WEBSITE_SIZE = 500  # Minimal webpage size in bytes


def same_domain(url1, url2):
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    domain1 = parsed1.netloc if not parsed1.netloc.startswith('www.') else parsed1.netloc[4:]
    domain2 = parsed2.netloc if not parsed2.netloc.startswith('www.') else parsed2.netloc[4:]
    return domain1 == domain2


def url_valid(url):
    if not isinstance(url, basestring):
        return False
    regex = re.compile(
        r'^https?://'  # http:// or https://
        # domain ...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)


class UrlChecker(object):
    OK = 0
    OK_MOVED = 1
    ERROR = 2
    PARKING = 3
    INVALID_URL = 4

    DEFAULT_TIMEOUT = 8

    moved_to_url = None

    def __init__(self, url, timeout=DEFAULT_TIMEOUT):
        self.url = url
        self.timeout = timeout
        self.status = self.check_url()

    @property
    def is_working(self):
        return self.status in (self.OK, self.OK_MOVED, self.PARKING)

    @property
    def is_valid(self):
        return self.status != self.INVALID_URL

    @property
    def is_parking(self):
        return self.status == self.PARKING

    @property
    def new_url(self):
        return self.moved_to_url

    def check_url(self):
        if not url_valid(self.url):
            return self.INVALID_URL
        data = ""
        try:
            res = requests.get(self.url, timeout=self.timeout, headers={
                # TODO better user-agent handling
                'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"
            })
        except requests.exceptions.RequestException:
            return self.ERROR

        if res.status_code != 200:
            return self.ERROR

        data = res.text

        udata = re.sub(r'\s+', ' ', data)
        if len(udata) < MIN_WEBSITE_SIZE:
            return self.PARKING

        for phrase in PARKED_PHRASES:
            if re.search(phrase, data, flags=re.I) is not None:
                return self.PARKING

        if res.history:
            for history in res.history:
                if not same_domain(self.url, history.url):
                    self.moved_to_url = res.history[-1].url
                    return self.OK_MOVED

        return self.OK
