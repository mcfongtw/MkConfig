Release History
===============
**0.1**
- Released on Apr. 2017
- This release focuses on finalizing the implementation of generating Collectd-GenericJMX 
configuration. Some optimizations are also implemented to its internal transformative operations,
 including
    * Redundant *MBean* definitions are removed, since the common *MBean* definitions is 
    processed as a independent step as well as the *MBean* definition is generally overridable due to 
    new hierarchical model.
    * Performance improvement on centralizing *MBean* and *Connection* blocks in a global *Plugin* 
    block. 
- In addition, a initial support to [FastJmx][2] and is considered as a variant to Collectd config 
type; Collectd-FastJmx. 
- More design documents is provided via Sphinx Document Generator.


**0.1-beta**
- Released on Feb. 2017
- This release focuses on internal integration with Jenkins to realize simple form of Continuous 
Integration. 
- Additionally, a standard setup procedure (via setuptools) is defined.
- Simplify the meta and logic for generating Collectd-GenericJmx config. 

**0.1-alpha**
- Released on Jan. 2017
- This release focuses on features of generating Collectd-GenericJMX config.
- The use case aims to support Collectd monitoring java applications via exporting JMX metrics. For more information, please refer to [Collectd GenericJMX Plugin] [1]
- Technology wise, we adopt several common python framework, including Jinja2 template engine, Cement CLI framework, read/write from yaml file.

[1]: https://collectd.org/wiki/index.php/Plugin:GenericJMX
[2]: https://github.com/egineering-llc/collectd-fast-jmx
