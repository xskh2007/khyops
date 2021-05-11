#!/bin/bash
tar zxvf acme.sh.tar.gz 
cd /root/acme.sh
./acme.sh --install
echo 'alias acme.sh=~/.acme.sh/acme.sh' >>/etc/profile
source /etc/profile
echo "acme安装完毕"

#myFile="etc/nginx/sites-enabled/default"

#if [ ! -f "$myFile" ]; then
#    \cp /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
#fi
#killall nginx
#/usr/sbin/nginx -s reload
#rm -f /etc/nginx/sites-enabled/default

File-nginx-wlhy="etc/nginx/sites-enabled/nginx-wlhy.conf"
if [ -f "${File-nginx-wlhy}" ]; then
    rm -f  /etc/nginx/sites-available/nginx-wlhy.conf
fi


domain=$1
iswww=$2
if (( $iswww == 1 ))
then
    echo "开始生成ssl证书，不生成www"
    echo $iswww
    /root/.acme.sh/acme.sh --issue -d www.$domain --webroot /var/www/html --force
    /root/.acme.sh/acme.sh --issue -d wlhy.$domain --webroot /var/www/html --force
    /root/.acme.sh/acme.sh --issue -d bops.$domain --webroot /var/www/html --force
    /root/.acme.sh/acme.sh --issue -d driver.$domain --webroot /var/www/html --force



    /root/.acme.sh/acme.sh --installcert -d www.$domain --key-file /etc/nginx/ssl/www.$domain.key --fullchain-file /etc/nginx/ssl/www.$domain.cer
    /root/.acme.sh/acme.sh --installcert -d wlhy.$domain --key-file /etc/nginx/ssl/wlhy.$domain.key --fullchain-file /etc/nginx/ssl/wlhy.$domain.cer
    /root/.acme.sh/acme.sh --installcert -d bops.$domain --key-file /etc/nginx/ssl/bops.$domain.key --fullchain-file /etc/nginx/ssl/bops.$domain.cer
    /root/.acme.sh/acme.sh --installcert -d driver.$domain --key-file /etc/nginx/ssl/driver.$domain.key --fullchain-file /etc/nginx/ssl/driver.$domain.cer

    #\cp /root/.acme.sh/www.$domain/www.$domain.cer /etc/nginx/ssl/
    #\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.cer /etc/nginx/ssl/
    #\cp /root/.acme.sh/bops.$domain/bops.$domain.cer /etc/nginx/ssl/
    #\cp /root/.acme.sh/driver.$domain/driver.$domain.cer /etc/nginx/ssl/

    #\cp /root/.acme.sh/www.$domain/www.$domain.key /etc/nginx/ssl/
    #\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.key /etc/nginx/ssl/
    #\cp /root/.acme.sh/bops.$domain/bops.$domain.key /etc/nginx/ssl/
    #\cp /root/.acme.sh/driver.$domain/driver.$domain.key /etc/nginx/ssl/
else
    echo "开始生成ssl证书，生成www"
    echo $iswww
    /root/.acme.sh/acme.sh --issue -d wlhy.$domain --webroot /var/www/html --force
    /root/.acme.sh/acme.sh --issue -d bops.$domain --webroot /var/www/html --force
    /root/.acme.sh/acme.sh --issue -d driver.$domain --webroot /var/www/html --force

    /root/.acme.sh/acme.sh --installcert -d wlhy.$domain --key-file /etc/nginx/ssl/wlhy.$domain.key --fullchain-file /etc/nginx/ssl/wlhy.$domain.cer
    /root/.acme.sh/acme.sh --installcert -d bops.$domain --key-file /etc/nginx/ssl/bops.$domain.key --fullchain-file /etc/nginx/ssl/bops.$domain.cer
    /root/.acme.sh/acme.sh --installcert -d driver.$domain --key-file /etc/nginx/ssl/driver.$domain.key --fullchain-file /etc/nginx/ssl/driver.$domain.cer

    #\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.cer /etc/nginx/ssl/
    #\cp /root/.acme.sh/bops.$domain/bops.$domain.cer /etc/nginx/ssl/
    #\cp /root/.acme.sh/driver.$domain/driver.$domain.cer /etc/nginx/ssl/

    #\cp /root/.acme.sh/wlhy.$domain/wlhy.$domain.key /etc/nginx/ssl/
    #\cp /root/.acme.sh/bops.$domain/bops.$domain.key /etc/nginx/ssl/
    #\cp /root/.acme.sh/driver.$domain/driver.$domain.key /etc/nginx/ssl/fi
fi


#domain=$1
#acme.sh --issue  -d $domain  --nginx

service nginx restart