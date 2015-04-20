from unittest import TestCase
import os
import shutil

from django.template import Template, Context, TemplateSyntaxError

from offlinecdn.conf import settings
from offlinecdn.templatetags.offlinecdn import OfflineCdnNode

cached_dir = settings.OFFLINE_STATIC_ROOT


class CssTest(TestCase):
    def setUp(self):
        settings.OFFLINECDN_MODE = True
        if os.path.exists(cached_dir):
            shutil.rmtree(cached_dir)

    def test_cached(self):
        rendered = self.get_template().render(Context({}))
        self.assertNotIn("cdnjs", rendered)
        self.assertTrue(os.path.exists(cached_dir))
        node = OfflineCdnNode("", "")
        node.reformat_url((self.cdn + self.package)[1:-1])

    def test_not_cached(self):
        settings.OFFLINECDN_MODE = False
        rendered = self.get_template().render(Context({}))
        self.assertIn("cdnjs", rendered)
        self.assertFalse(os.path.exists(cached_dir))

    cdn = '"https://cdnjs.cloudflare.com/ajax/libs/'
    package = 'twitter-bootstrap/3.3.4/css/bootstrap.min.css"'

    def get_template(self):
        template_string = """
        {% load offlinecdn %}
        {% offlinecdn css %}
        <link href=""" + self.cdn + self.package + """>
        {% endofflinecdn %}
        """
        return Template(template_string)


class SlashSlashTest(CssTest):
    cdn = '"//cdnjs.cloudflare.com/ajax/libs/'


# class NoSlashTest(BaseTest):
#     cdn = '"cdnjs.cloudflare.com/ajax/libs/'


class JsTest(CssTest):
    cdn = '"https://cdnjs.cloudflare.com/ajax/libs/'
    package = 'ember.js/1.11.3/ember.min.js"'

    def get_template(self):
        template_string = """
        {% load offlinecdn %}
        {% offlinecdn js %}
        <script src=""" + self.cdn + self.package + """></script>
        {% endofflinecdn %}
        """
        return Template(template_string)


class TwoPackageTest(JsTest):
    other_cdn = SlashSlashTest.cdn

    def get_template(self):
        moment = 'moment.js/2.10.2/moment.min.js"'
        template_string = """
        {% load offlinecdn %}
        {% offlinecdn js %}
        <script src=""" + self.cdn + self.package + """></script>
        <script src=""" + self.other_cdn + moment + """></script>
        {% endofflinecdn %}
        """
        return Template(template_string)

    def test_cached(self):
        rendered = self.get_template().render(Context({}))
        self.assertNotIn("cdnjs", rendered)
        self.assertTrue(os.path.exists(cached_dir))


class OfflineTests(TestCase):
    cdn = '"https://cdnjs.cloudflare.com/ajax/libs/'
    package = 'moment.js/2.10.2/moment.min.js"'

    def test_reformatted(self):
        node = OfflineCdnNode("", "")
        reformatted = node.reformat_url((self.cdn + self.package)[1:-1])
        self.assertNotIn("cdnjs", reformatted)

    def test_bad_template(self):
        moment = 'moment.js/2.10.2/moment.min.js"'
        template_string = """
        {% load offlinecdn %}
        {% offlinecdn cs %}
        <script src=""" + self.cdn + self.package + """></script>
        <script src=""" + SlashSlashTest.cdn + moment + """></script>
        {% endofflinecdn %}
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(template_string)

# css or JS, not something else
# reformat_url
# strip_leading_slash
# process_tags
# nodes = template.nodelist.get_nodes_by_type(OfflineCdnNode)
