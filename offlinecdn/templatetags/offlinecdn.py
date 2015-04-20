import urlparse
import os

from django import template
from bs4 import BeautifulSoup
import requests

from ..conf import settings
from .. import exceptions

register = template.Library()


@register.tag
def offlinecdn(parser, token):
    """this is the compiler for the CustomTemplateTag. It reads in until
    ``endofflinecdn`` and then renders each node.

    """
    nodelist = parser.parse(('endofflinecdn',))
    tag_declaration = token.split_contents()
    if len(tag_declaration) != 2 or tag_declaration[1] not in ('css', 'js'):
        raise template.TemplateSyntaxError(
            "offlinecdn takes exactly 1 argument (e.g. css or js)"
        )
    css_or_js = tag_declaration[1]
    parser.delete_first_token()
    return OfflineCdnNode(css_or_js, nodelist)


class OfflineCdnNode(template.Node):
    """IF OFFLINECDN_MODE=True, will do the following:

    - check to see if the cdn file is local
    - if it's not, download it
    - change the dom to reference the downloaded file
    """

    def __init__(self, css_or_js, nodelist):
        self.language = css_or_js
        self.nodelist = nodelist

    def render(self, context):
        html = self.nodelist.render(context)
        if not settings.OFFLINECDN_MODE:
            return html

        soup = BeautifulSoup(html)
        if self.language == 'css':
            return self.process_link_tags(soup)
        else:
            return self.process_script_tags(soup)

    def process_link_tags(self, soup):
        return self.process_tags(soup, "link", "href")

    def process_script_tags(self, soup):
        return self.process_tags(soup, "script", "src")

    def process_tags(self, soup, tag_name, tag_attr):
        """Check to see if ``tag_name`` is cached locally and cache it, if
        not.  Then, modify attribute ``tag_attr`` in each HTML tag
        ``tag_name`` from ``soup``.

        """
        for tag in soup.find_all(tag_name):
            url_value = tag[tag_attr]
            self.cache_if_necessary(url_value)
            tag[tag_attr] = self.reformat_url(url_value)
        return soup.prettify()

    def strip_leading_slash(self, url_value):
        """remove the leading slash on the url to be compatible with the
        offline.conf.settings variables.
        """
        if url_value.startswith('/'):
            return url_value[1:]
        return url_value

    def reformat_url(self, url_value):
        """strip the scheme and domain from the url object and append the path
        to OFFLINECDN_STATIC_URL.
        """
        url = urlparse.urlparse(url_value)
        if url.scheme or url.netloc:
            urlparts = list(url)
            urlparts[0] = urlparts[1] = ""
            urlparts[2] = self.strip_leading_slash(urlparts[2])
            urlparts[2] = settings.OFFLINECDN_STATIC_URL + urlparts[2]
            url = urlparse.ParseResult(*urlparts)
        return url.geturl()

    def cache_if_necessary(self, url_value):

        url = urlparse.urlparse(url_value)
        urlparts = list(url)

        # check if the file has already been downloaded locally
        path_string = self.strip_leading_slash(urlparts[2])
        local_path = os.path.join(*path_string.split("/"))
        local_path = os.path.join(settings.OFFLINECDN_STATIC_ROOT, local_path)
        if os.path.exists(local_path):
            return
        else:
            os.makedirs(os.path.dirname(local_path))

        # if the url starts with '//', need to set the scheme before
        # we try and download some stuff
        if url_value.startswith('//'):
            url_value = 'http:' + url_value

        # download the file and store it locally
        response = requests.get(url_value, stream=True)
        if not response.ok:
            raise exceptions.DownloadError(url_value)
        with open(local_path, 'w') as stream:
            for line in response.iter_lines():
                if line:
                    stream.write(line)
