LoadPlugin java

<Plugin "java">
    #JVMARG "-verbose:jni"
    #JVMARG "-Xmx128m"
    JVMARG "-Djava.class.path=/usr/share/collectd/java/collectd-api.jar:{{ pathToCollectdFastJmxJar }}"

    LoadPlugin "com.e_gineering.collectd.FastJMX"

    <Plugin "FastJMX">

        MaxThreads 256
        CollectInternal true