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

curl -c /tmp/cicj -XGET "${URL_BASE}/step1.php" > /dev/null 2>&1
chmod 640 /tmp/cicj
curl -b /tmp/cicj -XGET "${URL_BASE}/step2.php" > /dev/null 2>&1
curl -b /tmp/cicj -XGET "${URL_BASE}/step3.php" > /dev/null 2>&1

if [ ! -z $CENTENGINE ]; then
    curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step3.php" --data "MONITORING_ENGINE=centreon-engine&INSTALL_DIR_ENGINE=${INSTALL_DIR_ENGINE}&CENTREON_ENGINE_STATS_BINARY=${CENTREON_ENGINE_STATS_BINARY}&MONITORING_VAR_LIB=${MONITORING_VAR_LIB}&CENTREON_ENGINE_CONNECTORS=${CENTREON_ENGINE_CONNECTORS}&CENTREON_ENGINE_LIB=${CENTREON_ENGINE_LIB}&EMBEDDED_PERL="
elif [ ! -z $NAGIOS ]; then
    curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step3.php" --data "MONITORING_ENGINE=nagios&INSTALL_DIR_NAGIOS=${INSTALL_DIR_NAGIOS}&NAGIOSTATS_BINARY=${NAGIOSTATS_BINARY}&NAGIOS_IMG=${NAGIOS_IMG}&EMBEDDED_PERL=${EMBEDDED_PERL}" > /dev/null 2>&1
fi

curl -b /tmp/cicj -XGET "${URL_BASE}/step4.php" > /dev/null 2>&1
if [ ! -z $CENTBROKER ]; then
    curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step4.php" --data "BROKER_MODULE=centreon-broker&CENTREONBROKER_ETC=${CENTREONBROKER_ETC}&CENTREONBROKER_CBMOD=${CENTREONBROKER_CMOD}&CENTREONBROKER_LOG=${CENTREONBROKER_LOG}&CENTREONBROKER_VARLIB=${CENTREONBROKER_VARLIB}&CENTREONBROKER_LIB=${CENTREONBROKER_LIB}"
elif [ ! -z $NDO ]; then
    curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step4.php" --data "BROKER_MODULE=ndoutils&NDOMOD_BINARY=${NDOMOD_BINARY}"
fi

curl -b /tmp/cicj -XGET "${URL_BASE}/step5.php" > /dev/null 2>&1
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step5.php" --data "ADMIN_PASSWORD=${LOG_ADMIN_PW}&confirm_password=${LOG_ADMIN_PW}&firstname=${LOG_ADMIN}&lastname=${LOG_ADMIN}&email=root%40localhost" > /dev/null 2>&1
curl -b /tmp/cicj -XGET "${URL_BASE}/step6.php" > /dev/null 2>&1
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step6.php" --data "ADDRESS=${DB_ADDRESS}&DB_PORT=${DB_PORT}&root_password=${DB_ROOT_PW}&CONFIGURATION_DB=${DB_CONF_NAME}&STORAGE_DB=${DB_STORE_NAME}&UTILS_DB=${DB_UTIL_NAME}&DB_USER=${DB_CENT_USR}&DB_PASS=${DB_CENT_PW}&db_pass_confirm=${DB_CENT_PW}" > /dev/null 2>&1
curl -b /tmp/cicj -XGET "${URL_BASE}/step7.php" > /dev/null 2>&1
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/installConfigurationDb.php" --data ""
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/installStorageDb.php" --data ""
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/installUtilsDb.php" --data ""
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/createDbUser.php" --data ""
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/insertBaseConf.php" --data ""
curl -b /tmp/cicj -XPOST "${URL_BASE}/process/configFileSetup.php" --data ""
curl -b /tmp/cicj -XGET "${URL_BASE}/step8.php" > /dev/null 2>&1
rm -f /tmp/cicj
