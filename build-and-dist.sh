#!/bin/bash
#
# Build and source distribution tool for project 'MkConfig'
# 

CURRENT_WORKSPACE_PATH=$PWD
PY_ENV_HOME=$CURRENT_WORKSPACE_PATH/.py_env

PKG_NAME=mkconfig
PKG_VER=0.1b0


SETUP_BUILD_PATH=$CURRENT_WORKSPACE_PATH/build
SETUP_DIST_PATH=$CURRENT_WORKSPACE_PATH/dist
SETUP_DIST_SRC_PATH=$CURRENT_WORKSPACE_PATH/$PKG_NAME-$PKG_VER

# Delete previously built virtualenv
if [ -d $PY_ENV_HOME ]; 
then
	rm -rf $PY_ENV_HOME
fi
# Create virtualenv and install necessary packages
mkdir -p $PY_ENV_HOME

echo '==============================================='
echo 'Before everything begins, where am I?'
echo '-----------------------------------------------'
echo $CURRENT_WORKSPACE_PATH
echo '==============================================='
echo 


echo '==============================================='
echo 'Create virtualenv at ' $PY_ENV_HOME
echo '-----------------------------------------------'
virtualenv --no-site-packages $PY_ENV_HOME
# Activate the virtual env
source $PY_ENV_HOME/bin/activate
echo '==============================================='
echo 


echo '==============================================='
echo 'Install build-src required libraries'
echo '-----------------------------------------------'
pip install jinja2
pip install pyYAML
pip install cement

pip freeze
echo '==============================================='
echo 


#echo '==============================================='
#echo 'Install build-doc required libraries'
#echo '-----------------------------------------------'
#pip install sphinx
#echo '==============================================='
#echo 

echo '==============================================='
echo "setup.py sdist -k"
echo '-----------------------------------------------'
if [ -d $SETUP_DIST_PATH ]; 
then
	rm -rf $SETUP_DIST_PATH
fi
if [ -d $SETUP_DIST_SRC_PATH ]; 
then
	rm -rf $SETUP_DIST_SRC_PATH
fi
python setup.py sdist -k
tree $SETUP_DIST_SRC_PATH
echo '==============================================='
echo 


echo '==============================================='
echo "setup.py build"
echo '-----------------------------------------------'
if [ -d $SETUP_BUILD_PATH ]; 
then
	rm -rf $SETUP_BUILD_PATH
fi
python setup.py build
tree $SETUP_BUILD_PATH
echo '==============================================='
echo 


echo '==============================================='
echo "setup.py install"
echo '-----------------------------------------------'
python setup.py install
pip show $PKG_NAME
pip freeze
echo '==============================================='
echo 


echo '==============================================='
echo 'Install test required libraries'
echo '-----------------------------------------------'
pip install nosexcover
echo '==============================================='
echo 


echo '==============================================='
echo 'Perform nosetests '
echo '-----------------------------------------------'
cd $CURRENT_WORKSPACE_PATH/mkconfig/tests/
nosetests --with-xcoverage --with-xunit --cover-package=mkconfig.conf --cover-package=mkconfig.core --cover-inclusive
echo '==============================================='
echo 


echo '==============================================='
echo 'Testing executable binaries'
echo '-----------------------------------------------'
cd $CURRENT_WORKSPACE_PATH
rm /tmp/output.out
mkconfig -scassandra -o/tmp/output.out -dmkconfig/examples/
cat /tmp/output.out
echo '==============================================='
echo 


echo '==============================================='
echo 'Exit..Bye bye!'
echo '-----------------------------------------------'
deactivate
echo '==============================================='
