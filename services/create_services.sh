#!/bin/bash 


# ебучий виндус подставляет символ \r
# чтобы это дело убрать-почистить рекомендуется команда
# tr -d "\r" < create_services.sh > create_services_2.sh

rm -rf /home/teremok/services
cp -r /tmp/services /home/teremok/

rm /tmp/cron.photo.jpeg
rm /tmp/cron.screenshot.jpg

mkdir /home/teremok/screenshots
chown -R teremok /home/teremok/screenshots

#rm /etc/supervisor/conf.d/screenshots.conf
#rm /etc/supervisor/conf.d/photos.conf

cp /home/teremok/services/forsupervisor/screenshots.conf /etc/supervisor/conf.d/screenshots.conf
cp /home/teremok/services/forsupervisor/photos.conf /etc/supervisor/conf.d/photos.conf

chown -R teremok /home/teremok/services
