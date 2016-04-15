# -*- coding: utf-8 -*-
from unittest import TestCase
#from unittest import TestCase
from mock import patch, Mock

from requests.exceptions import RequestException

from urlchecker.url_checker import check_url, MIN_WEBSITE_SIZE, same_domain, UrlStatus

DEFAULT_URL = "http://test.com"


class TestUrlMatcher(TestCase):

    def test_same_domain_https(self):
        url1 = "https://test.com"
        url2 = "http://test.com"
        res = same_domain(url1, url2)
        assert res

    def test_same_domain_www(self):
        url1 = "http://www.test.com"
        url2 = "http://test.com"
        res = same_domain(url1, url2)
        assert res

    def test_same_domain_combination(self):
        url1 = "https://www.test.com"
        url2 = "http://test.com"
        res = same_domain(url1, url2)
        assert res


class TestUrlChecker(TestCase):

    def test_invalid_url_none(self):
        status = check_url(None)
        assert status == UrlStatus.INVALID_URL

    def test_invalid_url_str(self):
        status = check_url("http://http://test.com")
        assert status == UrlStatus.INVALID_URL

    def test_ioerror(self):
        with patch('requests.get') as retrieve_func:
            retrieve_func.side_effect = RequestException("some error")
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.ERROR

    def test_wrong_status(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 500
            stream_mock.history = []
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.ERROR

    def test_too_small_web(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = "       "
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_redirect_found(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200

            history_request = lambda: None
            history_request.status_code = 302
            history_request.url = "http://test.com"
            stream_mock.history = [history_request]
            stream_mock.text = 'a' * MIN_WEBSITE_SIZE

            retrieve_func.return_value = stream_mock
            status = check_url("http://www.test.com")
            assert status == UrlStatus.OK

    def test_redirect_internal(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200

            history_request = lambda: None
            history_request.status_code = 307
            history_request.url = "https://www.test.com"
            stream_mock.history = [history_request]
            stream_mock.text = 'a' * MIN_WEBSITE_SIZE

            retrieve_func.return_value = stream_mock
            status = check_url("http://www.test.com")
            assert status == UrlStatus.OK

    def test_redirect_permanent(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200

            history_request = lambda: None
            history_request.status_code = 301
            history_request.url = "http://test.com"
            stream_mock.history = [history_request]
            stream_mock.text = 'a' * MIN_WEBSITE_SIZE

            retrieve_func.return_value = stream_mock
            status = check_url("http://www.test.com")
            assert status == UrlStatus.OK

    def test_redirect_different_domain(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200

            history_request = lambda: None
            history_request.status_code = 301
            history_request.url = "http://completely.different.com"
            stream_mock.history = [history_request]
            stream_mock.text = 'a' * MIN_WEBSITE_SIZE

            retrieve_func.return_value = stream_mock
            status = check_url("http://www.test.com")
            assert status == UrlStatus.MOVED

    def test_parking_godaddy(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <!DOCTYPE html><body style="padding:0; margin:0;"><html><body><iframe src="http://mcc.godaddy.com/park/MzAhnzSiqzWapaO1YaOvrt==" style="visibility: visible;height: 100%; position:absolute" allowtransparency="true" marginheight="0" marginwidth="0" frameborder="0" width="100%"></iframe></body></html>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_for_sale(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <title>zhiyoujie.com域名出售，zhiyoujie.com可以转让，this domain is for sale</title>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_name_for_sale(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <title>zhiyoujie.com域名出售，zhiyoujie.com可以转让，this domain name is for sale</title>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_website_for_sale(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <title>website for sale</title>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_buy_this_domain(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            </script></head><body class="oneclick content" data-generated="21.04.15-12:49"><div id="header"><div class="domain "><h1>hottechtoday.com</h1></div><div class="buyBox"><h2><span><a target="_blank"  href="http://domains.latonas.com/buy/domain?domain=hottechtoday.com" >Buy this domain</a></span></h2><p><a target="_blank"  href="http://domains.latonas.com/buy/domain?domain=hottechtoday.com"  class="buyBoxTeaser">The domain <b>hottechtoday.com</b> may be for sale by its owner!</a></p></div></div><div id="content"><div id="left"></div><div id="center"><div id="webarchive"></div></div><div id="right"></div></div><div id="footer"><div id="search"><form id="searchform" action="http://ww21.hottechtoday.com/parking.php" method="get" name="searchform"><fieldset><input type="hidden" name="ses" value="Y3JlPTE0MzU2NjE3MzImdGNpZD13dzIxLmhvdHRlY2h0b2RheS5jb201NTkyNzVhNDAxMTU4NC42NzY1MDExMCZma2k9MjkzMTM5NDM4JnRhc2s9c2VhcmNoJmRvbWFpbj1ob3R0ZWNodG9kYXkuY29tJnM9ZTA4ZjEwNDc2NGM5OGYwMjM3NjkmbGFuZ3VhZ2U9ZW4mYV9pZD0xJnRyYWNrcXVlcnk9MQ==" class="formHidden" /><input type="hidden" name="token" value=""/><label><span>Search</span></label><input type="text" name="keyword" value="" id="searchtext" maxlength="70" /><button type="submit"><span><span>Search</span></span></button></fieldset></form></div><div id="disclaimer"><span class="sedologo"><a href="http://sedoparking.com/en" target="_blank"><img src="http://img.sedoparking.com/templates/brick_gfx/common/logo_white.png" alt="Sedo Logo"/></a></span><span class="text">This page provided to the domain owner <b>free</b> by Sedo's&nbsp;<a href="http://www.sedo.com/services/parking.php3?language=e&amp;partnerid=20293"title="Domain Parking">Domain Parking</a>. Disclaimer: Domain owner and Sedo maintain no relationship with third party advertisers. Reference to any specific service or trade mark is not controlled by Sedo or domain owner and does not constitute or imply its association, endorsement or recommendation.</span></div></div>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_sedoparking(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <a href="http://sedoparking.com/en" target="_blank"><img src="http://img.sedoparking.com/templates/brick_gfx/common/logo_white.png" alt="Sedo Logo"/></a>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_registrar_frameset(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <script type="text/javascript">registrar_frameset({a_id: 115576, drid: "as-drid-2578124767373827", frame: "ad_frame"});</script>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_has_expired(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
             This domain has expired and is now suspended. If you are the Registrant and
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING

    def test_parking_domain_parked(self):
        with patch('requests.get') as retrieve_func:
            stream_mock = Mock()
            stream_mock.status_code = 200
            stream_mock.history = []
            stream_mock.text = """
            <h3 class="muted">A really cool domain parked on <a id="parkio-link" href="http://park.io">park.IO</a></h3>
            """ + "a" * MIN_WEBSITE_SIZE
            retrieve_func.return_value = stream_mock
            status = check_url(DEFAULT_URL)
            assert status == UrlStatus.PARKING


