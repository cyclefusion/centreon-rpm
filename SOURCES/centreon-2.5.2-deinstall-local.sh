#!/bin/sh

. ${1}/configuration.sh

echo "drop database ${DB_CONF_NAME}; drop database ${DB_STORE_NAME}; drop database ${DB_UTIL_NAME};" | mysql -uroot -p${DB_ROOT_PW}
