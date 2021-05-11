#!/bin/bash

apt update -qq && apt install nginx unzip -y -qq
mkdir -p /etc/nginx/ssl
mkdir -p /var/www/html/
#\cp  /root/nginx-wlhy.conf /etc/nginx/sites-enabled/
#\cp /root/index.html /var/www/html/index.html

service nginx restart