from unittest import TestCase

from django.template import Context, Template
from django.template.base import VariableNode

class NodelistTest(TestCase):
    def test_for(self):
        template = Template('{% for i in 1 %}{{ a }}{% endfor %}')
        vars = template.nodelist.get_nodes_by_type(VariableNode)
        self.assertEqual(len(vars), 1)

    def test_if(self):
        template = Template('{% if x %}{{ a }}{% endif %}')
        vars = template.nodelist.get_nodes_by_type(VariableNode)
        self.assertEqual(len(vars), 1)

    def test_ifequal(self):
        template = Template('{% ifequal x y %}{{ a }}{% endifequal %}')
        vars = template.nodelist.get_nodes_by_type(VariableNode)
        self.assertEqual(len(vars), 1)

    def test_ifchanged(self):
        template = Template('{% ifchanged x %}{{ a }}{% endifchanged %}')
        vars = template.nodelist.get_nodes_by_type(VariableNode)
        self.assertEqual(len(vars), 1)
