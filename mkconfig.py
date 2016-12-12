#!/usr/bin/python
#

from conf.collectd import JmxTransifgurationChain
import logging
import env
import argparse

logger = logging.getLogger(__name__)

def do_main(args) :
    arg_props = args['props'];
    arg_mbeans = args['mbeans']
    arg_template = args['template']
    arg_output = args['output']

    logger.info('Mkconfig will execute based on [{}]'.format(args))

    context = {
        '_collectd_jmx_yaml_props_file': arg_props,
        '_collectd_jmx_yaml_mbeans_file': arg_mbeans,
        '_collectd_jmx_input': arg_template,
        '_collectd_jmx_output': arg_output
    }
    chain = JmxTransifgurationChain()
    chain.execute(context)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Configuration Automatically')
    parser.add_argument('-p', '--props', metavar='props', type=str, help='Input properties in yaml')
    parser.add_argument('-m', '--mbeans', metavar='mbeans', type=str, help='Input mbeans in yaml')
    parser.add_argument('-t', '--template', metavar='temp', type=str, default='collectd-jmx', help='configuration template type')
    parser.add_argument('-o', '--output', metavar='output', type=str, help='output files')

    args = vars(parser.parse_args())
    do_main(args);