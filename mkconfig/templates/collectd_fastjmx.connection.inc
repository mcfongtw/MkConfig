    # Beginning of Connection definition for {{ progName }} as of version {{ progVer }}
        <Connection>
            ServiceURL "service:jmx:rmi:///jndi/rmi://{{ hostAddr }}:{{ hostPort }}/jmxrmi"
            Host "{{ fqdn }}"
            InstancePrefix "{{ progPrefix }}"

            {% for collection in collections -%}
                {% if collection.secOrderSubstituion is defined -%}
            {% raw %} {% for item in {% endraw %} {{ collection.secOrderSubstituion }} {% raw %} -%} {% endraw %}
                {% endif -%}
            {% if collection.validated -%}
            Collect {{ collection.name }}
            {% else -%}
            #Collect {{ collection.name }}
            {% endif -%}
            {% if collection.secOrderSubstituion is defined -%}
          {% raw %} {% endfor %} {% endraw %}
            {% endif -%}
            {%- endfor %}

            {%- if timeToLive is defined %}
            ## Force the connection to reset every {{ timeToLive }} seconds
            TTL {{ timeToLive }}
            {% endif %}
        </Connection>
    # End of Connection definition for {{ progName }} as of version {{ progVer }}