# Deployment environment

This is based on a debian* linux distrib.

## prepare ##

```
sudo aptitude update
sudo aptitude upgrade
sudo aptitude install build-essential mysql-server libmysqlclient-dev curl zlib1g-dev libbz2-dev libssl-dev git-core
```

## Create deploy user ##

`USER` is the user name you want, it can be `deploy` which is quite common, or `openparty` specific for this project.

```
sudo -s
mkdir /home/USER
useradd -s /bin/bash -d /home/USER USER
passwd USER
usermod -a -G sshers USER
usermod -a -G sudoers USER
chown USER:USER /home/USER
```

## python ##

Login as that user you created.

```
curl -kL http://xrl.us/pythonbrewinstall | bash
```

Please add the following line to the end of your ~/.bashrc

```
[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source "$HOME/.pythonbrew/etc/bashrc"
```

## Setup ##

**Only run this for the very first time**

```
fab production setup_pythonbrew
fab production create_venv
fab production setup
```

## Deploy

**You can do this whenever you want, it's repeatable.

```
fab production deploy
```