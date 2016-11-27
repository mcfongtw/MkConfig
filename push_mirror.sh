#!/bin/bash - 
#===============================================================================
#
#          FILE: push_mirror.sh
# 
#         USAGE: ./push_mirror.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年10月15日 01時41分52秒
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

echo 'Checking Git config'
grep -A 5 'github' .git/config 

echo 'Start to mirror the commit to Github'
git push --mirror github
