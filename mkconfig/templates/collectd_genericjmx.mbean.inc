        # Beginning of JMX definition for {{ progName }} as of version {{ progVer }}
        {% for mbean in mbeans %}
            {% if mbean.collection is defined -%}
        {% raw %} {% for item in {% endraw %} {{ mbean.collection }} {% raw %} %} {% endraw %}
            {% endif -%}
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
            {% if mbean.collection is defined -%}
        {% raw %} {% endfor %} {% endraw %}
            {% endif -%}
        {% endfor %}
        # End of JMX definition for {{ progName }} as of version {{ progVer }}
