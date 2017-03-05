        # Beginning of JMX definition for {{ progName }} as of version {{ progVer }}
        <Connection>
            ServiceURL "service:jmx:rmi:///jndi/rmi://{{ hostAddr }}:{{ hostPort }}/jmxrmi"
            Host "{{ fqdn }}"
            InstancePrefix "{{ progPrefix }}"

            {% for mbean in mbeans -%}
                {% if mbean.collection is defined -%}
            {% raw %} {% for item in {% endraw %} {{ mbean.collection }} {% raw %} %} {% endraw %}
                {% endif -%}
                {% if mbean.required -%}
            Collect {{ mbean.name }}
                {% else -%}
            #Collect {{ mbean.name }}
                {% endif -%}
                {% if mbean.collection is defined -%}
            {% raw %} {% endfor %} {% endraw %}
                {% endif -%}
            {% endfor -%}
</Connection>
        # End of JMX definition for {{ progName }} as of version {{ progVer }}