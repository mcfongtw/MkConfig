    # Beginning of JMX definition for {{ progName }} as of version {{ progVer }}
        <Connection>
            ServiceURL "service:jmx:rmi:///jndi/rmi://{{ hostAddr }}:{{ hostPort }}/jmxrmi"
            Host "{{ fqdn }}"
            InstancePrefix "{{ progPrefix }}"

            {% for collection in collections -%}
                {% if collection.secOrderSubstituion is defined -%}
            {% raw %} {% for item in {% endraw %} {{ collection.secOrderSubstituion }} {% raw %} -%} {% endraw %}
                {% endif -%}
            Collect {{ collection.name }}
            {% if collection.secOrderSubstituion is defined -%}
          {% raw %} {% endfor %} {% endraw %}
            {% endif -%}
            {%- endfor %}
        </Connection>
    # End of JMX definition for {{ progName }} as of version {{ progVer }}