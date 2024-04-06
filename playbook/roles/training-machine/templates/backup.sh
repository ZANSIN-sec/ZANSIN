#!/bin/bash
period=60
array=("miniquest")
dirpath='/usr/local/dbbackup/'
filename=`date +%y%m%d%H%M`

{% raw %}
for ((i = 0; i < ${#array[@]}; i++)) {
  mysqldump --defaults-extra-file=/usr/local/dbbackup/mysqldump_backup.conf --ssl-mode=DISABLED --skip-column-statistics -h 127.0.0.1 ${array[i]} > $dirpath/${array[i]}_$filename.sql
  chmod 700 $dirpath/${array[i]}_$filename.sql
}
find /usr/local/dbbackup -maxdepth 1 -name \*.sql -mmin +$period -exec rm {} \;

{% endraw %}