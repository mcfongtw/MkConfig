    # Beginning of MBean definition for {{ progName }} as of version {{ progVer }}
        {% for mbean in mbeans %}
            {%- if mbean.secOrderSubstituion is defined %}
        {% raw %} {% for item in {% endraw %} {{ mbean.secOrderSubstituion }} {% raw %} -%} {% endraw %}
            {% endif %}
        <MBean "{{ mbean.name }}">
            ObjectName "{{ mbean.objectName }}"
            InstancePrefix "{{ mbean.InstancePrefix }}"
            {% for attribute in mbean.attributes %}
            <Value>
                {%- for key, value in attribute.items() %}
                    {{ key|e }} : {{ value|e }}
                {%- endfor %}
            </Value>
            {%- endfor %}
        </MBean>
            {%- if mbean.secOrderSubstituion is defined %}
        {% raw %} {% endfor %} {% endraw %}
            {% endif %}
        {% endfor -%}
    # End of MBean definition for {{ progName }} as of version {{ progVer }}
