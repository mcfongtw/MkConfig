Architecture
============

Concept Overview
----------------
Each supported configuration generation comes with a template (defined in mkconfig/templates/); and each
config is highly configurable since each config type comes with a unique set of meta files. For more high level
examples, please refer to sample meta file (under mkconfig/examples/). Internally, the tempalte engine support
templating strategy as of this version include [Jinja2](http://jinja.pocoo.org/docs/2.9/extensions/).

The next section introduce the current implementation of configuration transformation.


Transfiguration and Chaining Effect
------------------------------------
Transfiguration by definition is a change in form or appearance. We use this term to refer to configuration
transformation from an input to an output. As transformation logic becomes more complex, a new
form of 'series of transfigurations inside a transifguration' or 'Group transfiguration' is
sometimes needed. We refer this type of operaiton as 'Chain of transfiguration', also recognized
as another type of transfiguration, namely, 'ChainedTransfiguration'


Configuration Transfiguration
----------------------------
We adop the concept of ChainedTransfiguration heavily in the implementation. In addition, the
core technology to make transfiguration happened is using Jinja2 template engine. For currently
supported configuration, we could locate a list of Jinja2 template file under mkconfig/templates/
 package.

As of this release, we support the following configuration type:

*   Collectd-Jmx

    There are two types supported or Collectd-Jmx configuration generation:

    1. Collectd-GenericJmx : [https://collectd.org/wiki/index.php/Plugin:GenericJMX]
    2. Collectd-FastJmx : [https://github.com/egineering-llc/collectd-fast-jmx]

    Both of them follow the same transformation flow, but with different template in terms of format.

    * FullChainedTransfiguration
      Each call from cli component would perform a full cycle of FullChainedTransfiguration as shown in figure below:
    .. figure:: full_chain_of_transfiguration.png
     :scale: 100 %
     :alt: State Diagram of FullChainedTransfiguration

    * Each FullChainedTransfiguration contain several steps

      a. CommonMBeansChainedTransfiguration

         * Generate partial configuration for common mbean block
         * Each call would perform a cycle of transforming commonly used MBean blocks as shown in figure below
         .. figure:: common_mbean_chain_of_transfiguration.png
          :scale: 100 %
          :alt: State Diagram of CommonMBeansChainedTransfiguration
      b. SpliByApplicationTransfiguration

         * Inside there is a loop to generate application related partial configuration. Logically, this task would perform ApplicationChainedTransfiguration for each application

         * Each call from ApplicationChainedTransfiguration would perform a cycle of transforming MBean or Collection blocks for desginated application as shown in figure below
         .. figure:: application_chain_of_transfiguration.png
          :scale: 100 %
          :alt: State Diagram of ApplicationChainedTransfiguratio
         * For each ApplicationChainedTransfiguration, it would perform

           a. PrepareAppConfTransfiguration
           b. ConfReaderToContextTransfiguration
           c. ValidateCollectionTags
            * Validate the user defined collection mbeans. Commented out if the mbean name does not exist from MBean blocks available.
           d. AttributeChainedTransfiguration('mbean')
            * Generate partial configuration for application related MBean blocks
           e. AttributeChainedTransfiguration('connection')
            * Generate partial configuration for application related Collection block

      c. ConsolidateToFinalOutput
         * Consolidate all partial configuration into final output file


