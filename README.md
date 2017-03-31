Overview
========
MkConfig is a python package for generating complex configuration in a composable way with as little coding effort as
 possible. Each supported configuration generation comes with a template (defined in mkconfig/templates/); and each  
config is highly configurable since each config type comes with a set of meta files. As for currently supported  
configuration type, CollectdJmx - each meta file is exclusively specific for each target application to generate 
configuration for. For more high level examples, please refer to sample meta file (under mkconfig/examples/).

Internally, the tempalte engine support templating strategy as of this version include 
[Jinja2](http://jinja.pocoo.org/docs/2.9/extensions/). For more information about concept of design or config  
generation in technical details, please refer to Sphinx documents (under mkconfig/docs)   

Version
--------
0.1

Supported Configuration
-----------------------
Here are types of configuration supported :
1. CollectdJmx - [GenericJmx](https://collectd.org/wiki/index.php/Plugin:GenericJMX)
1. CollectdJmx - [FastJmx](https://github.com/egineering-llc/collectd-fast-jmx)

Library Dependency
------------------
Please refer to requirements.txt for details

Usage Guide
===========

Install Required Libraries
----------------------
If you have pip installed, run the following to install prerequisite dependencies, which is
defined in requirements.txt. You may try

`pip install -r requirements.txt`


Install Package
-----------
- Install via setup.py

    `python setup.py install`

CLI argument
------------
A transformation descriptor file defines configuration specific meta information, for instance, CollectdJmx may 
leverage bin/sample_collectd_jmx_control.yaml

mkconfig
- -i/--transf_desc_file: Path to transformation descriptor yaml file
- -o/--output: path to final output.
- -t/--template: (Optional) configuration type. Default is collectd_genericjmx

Sample Test
-----------
After this package is installed, run:

`mkconfig -o/tmp/output.conf -tcollectd_genericjmx -ibin/sample_collectd_jmx_control.yaml`

A sample output is generated at /tmp/output.conf. In adition, there are more examplified application meta file 
definition located under mkconfig/examples/



Development Guideline
=====================

Quality Code
-------------
All of the implementation should follow PEP-8 standard. This project is also evaluated with pyLint.

Install Pre-requisite Libraries
-------------------------------
Please make sure virtualenv package is installed, if not, try

`pip install virtualenv`

How to Build from Source
-------------------------
Execute the following script command
1. `./simulate clean`
2. `./simulate init`
2. `./simulate build`
3. `./simulate install`
