LoadPlugin java

<Plugin "java">
    #JVMARG "-verbose:jni"
    #JVMARG "-Xmx128m"
    JVMArg "-Djava.class.path=/usr/share/collectd/java/collectd-api.jar:/usr/share/collectd/java/generic-jmx.jar"

    LoadPlugin "org.collectd.java.GenericJMX"

    <Plugin "GenericJMX">