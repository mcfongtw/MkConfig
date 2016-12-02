import yaml
from conf.collectd import JmxTransifgurationChain
from unittest import TestCase

class TestCollectdJmxTransfiguration(TestCase):

    def test_integration_collectd_jmx_trans(self):
        context1 = {
            'progName' : 'TestJava',
            'hostName' : 'localhost',
            'hostPort' : '12345',
            'progVer' : '3.4561'
        }


        raw = open('cassandra_mbean.yaml').read()
        mbeans = []
        for raw_doc in raw.split('---'):
            try:
                mbeans.append(yaml.load(raw_doc))
            except SyntaxError:
                mbeans.append(raw_doc)

        context1['mbeans'] = mbeans

        context2 = {
            'cfs' : ['ap', 'apClient', 'event', 'alarm', 'indexEvent', 'indexTimeUUID', 'indexUTF8', 'statsAP', 'apConfig', 'wlanConfig'],
            'requests' : ['MutationStage', 'ReadRepairStage', 'ReadStage', 'ReplicateOnWriteStage', 'RequestResponseStage'],
            'internals' : ['FlushWriter', 'MemtablePostFlusher', 'commitlog_archiver', 'MigrationStage'],
            'drops' : ['MUTATION', 'COUNTER_MUTATION', 'READ_REPAIR', 'READ, REQUEST_RESPONSE'],
            'compaction_task_types' : ['CompletedTasks', 'PendingTasks']

        }

        chain = JmxTransifgurationChain()
        chain.prepare(context1, context2, 'collectd_jmx.template', 'collectd_jmx.conf')
        chain.execute()