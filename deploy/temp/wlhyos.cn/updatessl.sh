#!/bin/bash
 /root/.acme.sh/acme.sh --issue -d www.wlhyos.cn --webroot /var/www/html --force
 /root/.acme.sh/acme.sh --issue -d wlhy.wlhyos.cn --webroot /var/www/html --force
 /root/.acme.sh/acme.sh --issue -d bops.wlhyos.cn --webroot /var/www/html --force
 /root/.acme.sh/acme.sh --issue -d driver.wlhyos.cn --webroot /var/www/html --force
 /root/.acme.sh/acme.sh --installcert -d www.wlhyos.cn --key-file /etc/nginx/ssl/www.wlhyos.cn.key --fullchain-file /etc/nginx/ssl/www.wlhyos.cn.cer
 /root/.acme.sh/acme.sh --installcert -d wlhy.wlhyos.cn --key-file /etc/nginx/ssl/wlhy.wlhyos.cn.key --fullchain-file /etc/nginx/ssl/wlhy.wlhyos.cn.cer
 /root/.acme.sh/acme.sh --installcert -d bops.wlhyos.cn --key-file /etc/nginx/ssl/bops.wlhyos.cn.key --fullchain-file /etc/nginx/ssl/bops.wlhyos.cn.cer
 /root/.acme.sh/acme.sh --installcert -d driver.wlhyos.cn --key-file /etc/nginx/ssl/driver.wlhyos.cn.key --fullchain-file /etc/nginx/ssl/driver.wlhyos.cn.cer
 service nginx restart