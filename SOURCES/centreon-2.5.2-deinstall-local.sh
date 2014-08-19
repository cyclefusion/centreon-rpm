#!/bin/sh

. ${1}/configuration.sh

echo "Dropping all databases"
echo "drop database $DB_CONF_NAME;" | mysql -uroot -p${DB_ROOT_PW}
echo "drop database $DB_STORE_NAME;" | mysql -uroot -p${DB_ROOT_PW}
echo "drop database $DB_UTIL_NAME;" | mysql -uroot -p${DB_ROOT_PW}
