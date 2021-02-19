#!/bin/bash
tar zxvf acme.sh.tar.gz 
cd /root/acme.sh
./acme.sh --install
echo 'alias acme.sh=~/.acme.sh/acme.sh' >>/etc/profile
source /etc/profile

myFile="etc/nginx/sites-enabled/default"

if [ ! -f "$myFile" ]; then
    \cp /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
fi
/usr/sbin/nginx -s reload
rm -f /etc/nginx/sites-enabled/default


domain=$1
/root/.acme.sh/acme.sh --issue -d www.$domain --webroot /var/www/html --force
/root/.acme.sh/acme.sh --issue -d wlhy.$domain --webroot /var/www/html --force
/root/.acme.sh/acme.sh --issue -d weixin.wlhy.$domain --webroot /var/www/html --force
/root/.acme.sh/acme.sh --issue -d gate.wlhy.$domain --webroot /var/www/html --force

\cp /root/.acme.sh/www.$domain/www.$domain.cer /etc/nginx/ssl/
\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.cer /etc/nginx/ssl/
\cp /root/.acme.sh/weixin.wlhy.$domain/weixin.wlhy.$domain.cer /etc/nginx/ssl/
\cp /root/.acme.sh/gate.wlhy.$domain/gate.wlhy.$domain.cer /etc/nginx/ssl/

\cp /root/.acme.sh/www.$domain/www.$domain.key /etc/nginx/ssl/
\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.key /etc/nginx/ssl/
\cp /root/.acme.sh/weixin.wlhy.$domain/weixin.wlhy.$domain.key /etc/nginx/ssl/
\cp /root/.acme.sh/gate.wlhy.$domain/gate.wlhy.$domain.key /etc/nginx/ssl/

#domain=$1
#acme.sh --issue  -d $domain  --nginx

/usr/sbin/nginx -s reload
