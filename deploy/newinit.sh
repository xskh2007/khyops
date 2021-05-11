#!/bin/bash
domain=$1
company=$2
pid=$3

echo $1 >>/tmp/123
echo $2 >>/tmp/123
echo $3 >>/tmp/123



rm -rf temp/$domain

basedir=`cd $(dirname $0); pwd -P`
mkdir -p ${basedir}/temp/$domain
sed "s/__DOMAIN__/$domain/g;s/__PID__/$pid/g" ${basedir}/new-nginx-wlhy.conf > ${basedir}/temp/$domain/new-nginx-wlhy.conf
sed "s/__DOMAIN__/$domain/g;s/__PID__/$pid/g" ${basedir}/nowww-new-nginx-wlhy.conf > ${basedir}/temp/$domain/nowww-new-nginx-wlhy.conf

#cat ${basedir}/pack/init_index.html | sed "s@__COMPANY__@$company@;s@__WWW__@$icpurl@;" > ${basedir}/temp/$domain/index.html
#\cp install-nginx.sh temp/$domain/

