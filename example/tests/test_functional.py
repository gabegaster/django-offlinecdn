from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.template import Context, Template
from django.template.base import VariableNode

from offlinecdn.conf import settings


class StaticTest(StaticLiveServerTestCase):
    browser = None
    host = "http://localhost:8081"   # the LiveServerTestCase default

    def setUp(self):
        self.browser = webdriver.Firefox()
        settings.OFFLINECDN_MODE = True

    def test_server_running(self):
        r = requests.get(self.host)
        self.assertTrue(r.ok)

    def test_functional(self):
        self.browser.get(self.host)
        dom = self.browser.page_source
        soup = BeautifulSoup(dom)
        text = soup.find("h1").text
        self.assertNotIn("Hello, world!", text)

    def tearDown(self):
        self.browser.close()

# username = os.environ["SAUCE_USERNAME"]
# access_key = os.environ["SAUCE_ACCESS_KEY"]
# capabilities["tunnel-identifier"] = os.environ["TRAVIS_JOB_NUMBER"]
# hub_url = "%s:%s@localhost:4445" % (username, access_key)
# driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % hub_url)
