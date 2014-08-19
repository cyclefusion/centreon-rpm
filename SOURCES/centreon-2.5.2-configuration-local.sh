#!/bin/sh
URL_BASE="http://127.0.0.1/centreon/install/steps"

CENTENGINE=1
NAGIOS=

CENTBROKER=1
NDO=

INSTALL_DIR_NAGIOS=$(echo "/usr/local/nagios" | sed 's/\//%2F/g')
INSTALL_DIR_ENGINE=$(echo "/usr/local/centreon-full/" | sed 's/\//%2F/g')
CENTREON_ENGINE_STATS_BINARY=$(echo "/usr/local/centreon-full/bin/centenginestats" | sed 's/\//%2F/g')
MONITORING_VAR_LIB=$(echo "/var/lib/centreon-engine/" | sed 's/\//%2F/g')
CENTREON_ENGINE_CONNECTORS=$(echo "/usr/local/centreon-full/lib/" | sed 's/\//%2F/g')
CENTREON_ENGINE_LIB=$(echo "/usr/local/centreon-full/lib/centreon-engine/" | sed 's/\//%2F/g')
BROKER_MODULE=centreon-broker
CENTREONBROKER_ETC=$(echo "/etc/centreon-broker/" | sed 's/\//%2F/g')
CENTREONBROKER_CBMOD=$(echo "/usr/local/centreon-full/lib/cbmod.so" | sed 's/\//%2F/g')
CENTREONBROKER_LOG=$(echo "/var/log/centreon-broker/" | sed 's/\//%2F/g')
CENTREONBROKER_VARLIB=$(echo "/var/lib/centreon-broker/" | sed 's/\//%2F/g')
CENTREONBROKER_LIB=$(echo "/usr/local/centreon-full/lib/centreon-broker/" | sed 's/\//%2F/g')
NAGIOSTATS_BINARY=$(echo "/usr/local/nagios/bin/nagiostats" | sed 's/\//%2F/g')
NDOMOD_BINARY=$(echo "/usr/local/nagios/bin/ndomod.o" | sed 's/\//%2F/g')
NAGIOS_IMG=$(echo "/usr/local/nagios/share/images" | sed 's/\//%2F/g')
EMBEDDED_PERL=""
LOG_ADMIN_PW="admin"
LOG_ADMIN="admin"
DB_ADDRESS="127.0.0.1"
DB_PORT=3306
DB_ROOT_PW="root"
DB_CONF_NAME="centreon"
DB_STORE_NAME="centreon_storage"
DB_UTIL_NAME="centreon_status"
DB_CENT_USR="centreon"
DB_CENT_PW="centreon"
