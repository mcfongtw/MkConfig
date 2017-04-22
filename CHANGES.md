##0.1
- New Features
    * Initial support to FastJmx (MKCONFIG-38)
- Improvements
    * Support inheritance for MBean definitions (MKCONFIG-42)
    * Centralize common MBean definition as independent step (MKCONFIG-86)
    * Centralize <MBean/> and <Connection/> blocks in a global <Plugin/> block to reduce Collectd
     thread usage. (MKCONFIG-92)
    * Better documentation (MKCONFIG-22)
- Critical Bug Fixes
    * None

##0.1-beta
- New Features
    * Define setup procedure (MKCONFIG-12)
    * Jenkins integration to ensure project quality (MKCONFIG-15)
- Improvements
    * Enhance logger appender format and better descriptive message (MKCONFIG-19)
    * Consolidate Collectd-GenericJmx meta files into one for each application (MKCONFIG-34)
    * Organize attributes of Collectd-GenericJmx output. (MKCONFIG- 45)
    * Reconstruct project source repository for ease of setup. (MKCONFIG-80)
- Critical Bug Fixes
    * None

##0.1-alpha
- New Features
    * Implement a chain of transfiguration architecture (MKCONFIG-3)
    * Implement wrappers for several types of template engine (MKCONFIG-5)
    * Integrate and implement config generation for Collectd-GenericJMX (MKCONFIG-9)
    * Use Sphinx framework to manage and generate documentation (MKCONFIG-11)
    * Implement a basic set of CLI using Cement framework (MKCONFIG-13)
    * Provide example configurations for a set of Cassandra/Jenkins/Jira Jmx metrics (MKCONFIG-28)
    * Adopt MIT license (MKCONFIG-2)
- Improvements
    * None
- Critical Bug Fixes
    * None
