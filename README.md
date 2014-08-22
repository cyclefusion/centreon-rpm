# Centreon packages

Packages are available at http://repos.beastie.eu/CentOS6-x86_64-centreo/

```bash
wget http://repos.beastie.eu/CentOS6-x86_64-centreon/noarch/centreon-release-1-1.el6.noarch.rpm
rpm -i centreon-release-1-1.el6.noarch.rpm
yum update
```

## How to install a complete centreon

First, be sure to have a **working** MySQL database. I mean, `mysql_secure_installation` is ok and the `root password` is the same as defined in the install package `centreon-configuration-install-<install type>`.

```bash
yum install meta-centreon-central centreon-configuration-install-<install type>
```

Where `<install type>` is your custom (or not) package that installs scripts you have modified for your environment : remote MySQL database, custom passwords...

Then, ensure these services are started:

 * centcore
 * postfix
 * httpd
 * mysqld

## Issues

**For now, installation paths are not easily customisable**

There are multiple defines in scripts and SPEC files.

To avoid complex auto-detection in SPEC files, I think the best solution is to write a bit of `sed` commands.

**Everything has not been tested already**

I focus on creating packages that can give most flexibility for every environment. First issue apart :)

For now, I have pretty good results while installing a full centreon installation:

 * broker
 * engine
 * plugins
 * ssh keys (but no remote poller)
 * permissions on logs and directories
 * graphes

**To be tested**

 * A fresh install
 * Pollers
 * Upgrade: could be interesting to take a quite old version, for example 2.4, then upgrade to 2.5.x
