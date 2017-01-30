from mkconfig.core.jinja2 import Jinja2Engine
from jinja2 import DictLoader, Environment
import unittest
import yaml
from collections import OrderedDict
import logging
import mkconfig.env


logger = logging.getLogger(__name__)


class TestJinja2Engine(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_unit_basic_template(self):
        context = {'name' : 'John'}
        engine = Jinja2Engine()
        engine.init(DictLoader(dict(
            test="Hello World, {{ name }}"
        )))
        result = engine.apply(context, "test", None, True)
        self.assertEqual("Hello World, John", result)

    def test_unit_basic_mbean(self):
        yamlContent = """
        name : Cassandra_Memory
        objectName: java.lang:type=Memory
        InstancePrefix : Memory
        required: true
        attributes:
         - Attribute : HeapMemoryUsage
           InstancePrefix : Heap_Memory_Usage_
           Table : true
           Type : gauge
         - Attribute : NonHeapMemoryUsage
           InstancePrefix : Non_Heap_Memory_Usage_
           Table : true
           Type : gauge
        """

        mbeans = []
        mbeans.append(yaml.load(yamlContent))

        for mbean in mbeans:
            attributeList = []
            for attribute in mbean.get('attributes') :
                # print(attribute)
                ordered_attribute = OrderedDict(sorted(attribute.items(), key= lambda x : x[0]))
                # print('ordered : [{}]'.format(ordered_attribute))
                attributeList.append(ordered_attribute)
            mbean['attributes'] = attributeList

        context={'mbeans' : mbeans}
        logger.info('Context modified : '.format(str(context)))

        templateContent = """
        {% for mbean in mbeans %}
        <MBean "{{ mbean.name }}">
            ObjectName "{{ mbean.objectName }}"
            InstancePrefix "{{ mbean.InstancePrefix }}"
            {% for attribute in mbean.attributes -%}
            <Value>
                {% for key, value in attribute.items() -%}
                    {{ key|e }} : {{ value|e }}
                {% endfor -%}
            </Value>
            {% endfor -%}
        </MBean>
        {% endfor %}

        """
        engine = Jinja2Engine()
        engine.init(DictLoader(dict(test=templateContent)))
        actual = engine.apply(context, "test", None, True).replace(" ", "").replace("\n", "")

        expected="""
        <MBean "Cassandra_Memory">
            ObjectName "java.lang:type=Memory"
            InstancePrefix "Memory"
            <Value>
                Attribute : HeapMemoryUsage
                InstancePrefix : Heap_Memory_Usage_
                Table : True
                Type : gauge
                </Value>
            <Value>
                Attribute : NonHeapMemoryUsage
                InstancePrefix : Non_Heap_Memory_Usage_
                Table : True
                Type : gauge
                </Value>
            </MBean>
        """.replace(" ", "").replace("\n", "")

        self.maxDiff = None
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()