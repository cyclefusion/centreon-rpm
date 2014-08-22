# Centreon packages

Packages are available at http://repos.beastie.eu/CentOS6-x86_64-centreon/

You can create a custom repo file in `/etc/yum.repos.d/`:

```
[CentOS6-x86_64-centreon]
name=CentOS6-x86_64-centreon
baseurl=http://repos.beastie.eu/CentOS6-x86_64-centreon/
gpgcheck=0
enabled=1
```

First, be sure to have a **working** MySQL database. I mean, `mysql_secure_installation` is ok and the `root password` is the same as defined in the install package `centreon-configuration-install-<install type>`.

## How to install a complete centreon

```bash
yum install meta-centreon-central centreon-configuration-install-<install type>
```

Where `<install type>` is your custom (or not) package that installs scripts you have modified for your environment : remote MySQL database, custom passwords...

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
 * Upgrade: could be interesting to take a quite old version, for example 2.4, then upgrade to 2.5.x
