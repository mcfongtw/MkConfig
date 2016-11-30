from core.jinja2 import Jinja2Engine
from jinja2 import DictLoader, Environment
import unittest
import yaml
from collections import OrderedDict

class TestJinja2Engine(unittest.TestCase):

    def setUp(self):
        super(TestJinja2Engine, self).setUp()

    def assertEqualLongString(self, a, b):
        NOT, POINT = '-', '*'
        if a != b:
            print
            a
            o = ''
            for i, e in enumerate(a):
                try:
                    if e != b[i]:
                        o += POINT
                    else:
                        o += NOT
                except IndexError:
                    o += '*'

            o += NOT * (len(a) - len(o))
            if len(b) > len(a):
                o += POINT * (len(b) - len(a))

            print(o)
            print(b)

            raise AssertionError('(see string comparison above)')

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
        print(context)

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