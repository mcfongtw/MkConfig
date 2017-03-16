Design Documents Come Here
===========================
Overview
--------
This chapter include design document for current implementation of MkConfig


Transfiguration and Chainning Effect
------------------------------------
Transfiguration by definition is a change in form or appearance. We use this term to refer to configuration
transformation from input to final output. As transformation logic becomes more complex, a new form of
'transfigurations inside a transifguration' or 'Grouped transfiguration' is sometimes needed. We refer this type of
operaiton as 'Chain of transfiguration', also recognized as another type of transfiguration, namely,
'ChainedTransfiguration'


Supported Configuration Type
----------------------------

*   Collectd-Jmx

    There are two types supported or Collectd-Jmx configuration generation:

    1. Collectd-GenericJmx : [https://collectd.org/wiki/index.php/Plugin:GenericJMX]
    2. Collectd-FastJmx : [https://github.com/egineering-llc/collectd-fast-jmx]

    Both of them follows the same transformation flow

    * FullChainedTransfiguration
      Each call from cli component would perform a full cycle of FullChainedTransfiguration as shown in figure below:
    .. figure:: full_chain_of_transfiguration.png
     :scale: 100 %
     :alt: State Diagram of FullChainedTransfiguration

    * Each FullChainedTransfiguration contained several steps

      a. CommonMBeansChainedTransfiguration
      b. SpliByApplicationTransfiguration
      c. ConsolidateToFinalOutput

    * CommonMBeansChainedTransfiguration
      Each call would perform a cycle of transforming commonly used MBean blocks as shown in figure below
    .. figure:: common_mbean_chain_of_transfiguration.png
     :scale: 100 %
     :alt: State Diagram of CommonMBeansChainedTransfiguration

    * Each SpliByApplicationTransfiguration manages to perform ApplicationChainedTransfiguration for each application

    * For each ApplicationChainedTransfiguration, it would perform

      a. PrepareAppConfTransfiguration
      b. ConfReaderToContextTransfiguration
      c. ValidateCollectionTags
      d. AttributeChainedTransfiguration('mbean')
      e. AttributeChainedTransfiguration('connection')


    * ApplicationChainedTransfiguration
      Each call would perform a cycle of transforming MBean or Collection blocks for desginated application as shown in
      figure below
    .. figure:: application_chain_of_transfiguration.png
     :scale: 100 %
     :alt: State Diagram of ApplicationChainedTransfiguration