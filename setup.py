import os
from setuptools import setup, find_packages


# Utility function to read the README file.
def read(fname):
    try:
        f = open(os.path.join(os.path.dirname(__file__), fname), 'r')
    except IOError as e:
        errno, strerror = e.args
        print("I/O error! Code : ({0}) for [{1}]: {2}".format(errno, fname, strerror))
        raise
    else:
        result = f.read()
    return result


def install_requirement():
    content = read('requirements.txt')
    requirements = content.splitlines()
    print("-------------------")
    print(requirements)
    print("-------------------")
    return requirements

VERSION = '0.1'

setup_info = dict(
    # Metadata
    name='mkconfig',
    version=VERSION,
    author='Michael Fong',
    author_email='mcfong.open@gmail.com',
    url='https://github.com/mcfongtw',
#    download_url='',
    description='Make Configuration Utilities',
    long_description=read('README.md'),
    license='MIT',
    classifiers=[
        'Development Status :: Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    ###################################################################

    scripts=['bin/mkconfig', 'simulate'],

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[
    #    'templates/', ['.template']
    #],

    #This would work after making templats/ as a python package
    package_data={
        '' : ['*.template', '*.inc']
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = install_requirement(),

    # Package info
    packages = find_packages(exclude=['tests', 'docs', 'output', 'dist-src', 'build', '.*', 'mkconfig.egg-info']),


)

setup(**setup_info)
