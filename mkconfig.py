#!/usr/bin/python
#

from conf.collectd import JmxTransifgurationChain
import logging
import env
import argparse
import sys

logger = logging.getLogger(__name__)


def do_main(arg_props, arg_mbeans, arg_template, arg_output) :
    logger.info('Mkconfig will execute based on properties : [{}]'.format(arg_props))
    logger.info('Mkconfig will execute based on mbeans : [{}]'.format(arg_mbeans))
    logger.info('Mkconfig will execute based on template : [{}]'.format(arg_template))
    logger.info('Mkconfig will execute based on output : [{}]'.format(arg_output))

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

    arg_props = args['props'];
    arg_mbeans = args['mbeans']
    arg_template = args['template']
    arg_output = args['output']

    if arg_props is None or arg_mbeans is None or arg_template is None or arg_output is None:
        parser.print_help();

    do_main(arg_props, arg_mbeans, arg_template, arg_output)

    sys.exit(0)