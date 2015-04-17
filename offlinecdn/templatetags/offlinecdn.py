import urlparse

from django import template
from bs4 import BeautifulSoup

from ..conf import settings

register = template.Library()


@register.tag
def offlinecdn(parser, token):
    """this is the compiler for the CustomTemplateTag. It will read until
endofflinecdn and, IF debug=True, will do the following:

- check to see if the cdn file is local
- if it's not, download it
- change the dom to reference the downloaded file

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
    """
    """

    def __init__(self, css_or_js, nodelist):
        self.language = css_or_js
        self.nodelist = nodelist


    def filter_tags(self, soup, tag_name, tag_attr):
        for tag in soup.find_all(tag_name):
            url = urlparse.urlparse(tag[tag_attr])
            if url.scheme or url.netloc: 
                # make a new url
                urlparts = list(url)
                urlparts[0] = urlparts[1] = ""
                urlparts[2] = settings.OFFLINE_STATIC_URL + urlparts[2]
                new_url = urlparse.ParseResult(*urlparts)
                tag[tag_attr] = new_url
        return soup.prettify()

    def filter_link_tags(self, soup):
        return self.filter_tags(soup, "link", "href")

    def filter_script_tags(self, soup):
        return self.filter_tags(soup, "script", "src")

    def render(self, context):
        html = self.nodelist.render(context)
        soup = BeautifulSoup(html)
        if self.language == 'css':
            return self.filter_link_tags(soup)
        else:
            return self.filter_script_tags(soup)
