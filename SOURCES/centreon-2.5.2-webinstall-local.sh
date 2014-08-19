#!/bin/sh

. ${1}/configuration.sh

e_dbconf=$(echo "show databases;" | mysql -uroot -p${DB_ROOT_PW} | grep "${DB_CONF_NAME}")
e_dbstore=$(echo "show databases;" | mysql -uroot -p${DB_ROOT_PW} | grep "${DB_STORE_NAME}")
e_dbutil=$(echo "show databases;" | mysql -uroot -p${DB_ROOT_PW} | grep "${DB_UTIL_NAME}")

if [ ! -z $e_dbconf ]&&[ ! -z $e_dbstore ]&& [ ! -z $e_dbutil ]; then
    echo "This is an upgrade. No webinstall made. Do it yourself and remove install directory in centreon installation."
    exit 2
else
    echo "Dropping partial databases."
    echo "drop database $DB_CONF_NAME;" | mysql -uroot -p${DB_ROOT_PW}
    echo "drop database $DB_STORE_NAME;" | mysql -uroot -p${DB_ROOT_PW}
    echo "drop database $DB_UTIL_NAME;" | mysql -uroot -p${DB_ROOT_PW}
fi

curl -s -c /tmp/cicj -XGET "${URL_BASE}/step1.php" > /dev/null
chmod 640 /tmp/cicj
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step2.php" > /dev/null
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step3.php" > /dev/null

echo "Setup Monitoring Engine"
if [ ! -z $CENTENGINE ]; then
    curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step3.php" --data "MONITORING_ENGINE=centreon-engine&INSTALL_DIR_ENGINE=${INSTALL_DIR_ENGINE}&CENTREON_ENGINE_STATS_BINARY=${CENTREON_ENGINE_STATS_BINARY}&MONITORING_VAR_LIB=${MONITORING_VAR_LIB}&CENTREON_ENGINE_CONNECTORS=${CENTREON_ENGINE_CONNECTORS}&CENTREON_ENGINE_LIB=${CENTREON_ENGINE_LIB}&EMBEDDED_PERL="
elif [ ! -z $NAGIOS ]; then
    curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step3.php" --data "MONITORING_ENGINE=nagios&INSTALL_DIR_NAGIOS=${INSTALL_DIR_NAGIOS}&NAGIOSTATS_BINARY=${NAGIOSTATS_BINARY}&NAGIOS_IMG=${NAGIOS_IMG}&EMBEDDED_PERL=${EMBEDDED_PERL}"
fi

echo "Setup Broker"
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step4.php" > /dev/null
if [ ! -z $CENTBROKER ]; then
    curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step4.php" --data "BROKER_MODULE=centreon-broker&CENTREONBROKER_ETC=${CENTREONBROKER_ETC}&CENTREONBROKER_CBMOD=${CENTREONBROKER_CMOD}&CENTREONBROKER_LOG=${CENTREONBROKER_LOG}&CENTREONBROKER_VARLIB=${CENTREONBROKER_VARLIB}&CENTREONBROKER_LIB=${CENTREONBROKER_LIB}" 2> /dev/null
elif [ ! -z $NDO ]; then
    curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step4.php" --data "BROKER_MODULE=ndoutils&NDOMOD_BINARY=${NDOMOD_BINARY}" 2> /dev/null
fi

curl -s -b /tmp/cicj -XGET "${URL_BASE}/step5.php" > /dev/null
echo "Setup admin user:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step5.php" --data "ADMIN_PASSWORD=${LOG_ADMIN_PW}&confirm_password=${LOG_ADMIN_PW}&firstname=${LOG_ADMIN}&lastname=${LOG_ADMIN}&email=root%40localhost"
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step6.php" > /dev/null
echo "Setup database access:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/process_step6.php" --data "ADDRESS=${DB_ADDRESS}&DB_PORT=${DB_PORT}&root_password=${DB_ROOT_PW}&CONFIGURATION_DB=${DB_CONF_NAME}&STORAGE_DB=${DB_STORE_NAME}&UTILS_DB=${DB_UTIL_NAME}&DB_USER=${DB_CENT_USR}&DB_PASS=${DB_CENT_PW}&db_pass_confirm=${DB_CENT_PW}"
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step7.php" > /dev/null
echo "Setup ${DB_CONF_NAME} database:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/installConfigurationDb.php" --data ""
echo "Setup ${DB_STORE_NAME} database:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/installStorageDb.php" --data ""
echo "Setup ${DB_UTIL_NAME} database:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/installUtilsDb.php" --data ""
echo "Setup user:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/createDbUser.php" --data ""
echo "Setup configuration:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/insertBaseConf.php" --data ""
echo "Setup files:"
curl -s -b /tmp/cicj -XPOST "${URL_BASE}/process/configFileSetup.php" --data ""
echo "Installation end."
curl -s -b /tmp/cicj -XGET "${URL_BASE}/step8.php" > /dev/null
rm -f /tmp/cicj
