
# Deepin 20 编译安装 MySQL 5.7.25

> `MySQL` 是最流行的开源 `SQL` 数据库管理系统，由 `Oracle Corporation` 开发，分发和支持。`mysql` 下载地址：`https://dev.mysql.com/downloads/mysql/`
系统化境：Deepin 20

## 安装依赖

```
apt-get -y install make cmake gcc g++ bison openssl libssl-dev  libncurses5-dev
```

## 删除 my.conf 文件，如果有

```
rm -rf /etc/my.conf
```
## 创建用户

```
useradd -s /sbin/nologin mysql
```

## 下载源码包

```
wget https://cdn.mysql.com/archives/mysql-5.7/mysql-boost-5.7.25.tar.gz
```

## 解压

```
root@leo-PC:/home/leo/Downloads# tar -zxf mysql-boost-5.7.25.tar.gz
root@leo-PC:/home/leo/Downloads# ls -l
drwxr-xr-x 36 7161 31415      4096 12月 21  2018  mysql-5.7.25
-rw-r--r--  1 leo  leo    49107578 11月  2 18:22  mysql-boost-5.7.25.tar.gz
```

## 编译安装

```
root@leo-PC:/home/leo/Downloads# cd mysql-5.7.25/
root@leo-PC:/home/leo/Downloads/mysql-5.7.25# mkdir bld && cd bld
root@leo-PC:/home/leo/Downloads/mysql-5.7.25/bld# cmake ../ \
-DCMAKE_INSTALL_PREFIX=/opt/mysql/5.7.25 \
-DMYSQL_DATADIR=/opt/mysql/5.7.25/data \
-DSYSCONFDIR=/opt/mysql/5.7.25/etc \
-DMYSQL_TCP_PORT=3306 \
-DSYSTEMD_PID_DIR=/opt/mysql/5.7.25/mysqld.pid \
-DMYSQL_UNIX_ADDR=/opt/mysql/5.7.25/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_EXTRA_CHARSETS=all \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
-DWITH_ZLIB=bundled \
-DWITH_SSL=bundled \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_EMBEDDED_SERVER=0 \
-DENABLE_DOWNLOADS=1 \
-DWITH_DEBUG=0 \
-DWITH_BOOST=../boost/boost_1_59_0 \
-DWITH_SYSTEMD=1
...
...
-- Configuring done
-- Generating done
-- Build files have been written to: /home/leo/Downloads/mysql-5.7.25/bld

root@leo-PC:/home/leo/Downloads/mysql-5.7.25/bld# make && make install
```

## 配置文件 my.cnf

```
[mysqld]
port=3306
basedir=/opt/mysql/5.7.25
datadir=/opt/mysql/5.7.25/data
socket=/opt/mysql/5.7.25/mysql.sock
log-error=/opt/mysql/5.7.25/log/mysqld.log
pid-file=/opt/mysql/5.7.25/mysqld.pid
symbolic-links=0
max_allowed_packet=20M
default-time-zone = '+8:00'
bind_address='0.0.0.0'
character_set_server=utf8
collation_server=utf8_general_ci
autocommit=1
max_connections=1024
```

## 创建 log 目录

```
mkdir log
```

## 更改安装目录的所属用户为 mysql

```
chown -R mysql:mysql /opt/mysql/5.7.25/
```

## 初始化数据目录

```
bin/mysqld --initialize --user=mysql
```

## 生成的随即密码

```
cat log/mysqld.log | grep password
```

## 启动

```
bin/mysqld --daemonize --user=mysql
```

## 开机自动启动

```
cp ./support-files/mysql.server /etc/init.d/mysqld
```



# CentOS 7 源码安装 LNMP 之 MySQL 5.7.25

> MySQL是最流行的开源SQL数据库管理系统，由Oracle Corporation开发，分发和支持。

> `mysql` 下载地址：`https://dev.mysql.com/downloads/mysql/`

> 系统化境：`CentOS 7.6`


## 准备

### 安装依赖

```
[root@localhost Downloads]# yum install cmake ncurses  ncurses-devel gcc gcc-devel  gcc-c++
...
```

### 删除 my.cnf 文件，如果有

```
[root@localhost Downloads]# rm -rf /etc/my.cnf
```

### 创建用户

```
[root@localhost Downloads]# useradd -s /sbin/nologin mysql
```

### 下载源码包

```
[root@localhost Downloads]# wget https://cdn.mysql.com/archives/mysql-5.7/mysql-boost-5.7.25.tar.gz
```

## 解压

```
[root@localhost Downloads]# ls -l
-rw-rw-r--. 1 leo leo 49107578 7月   8 19:48 mysql-boost-5.7.25.tar.gz
[root@localhost Downloads]# tar -zxvf mysql-boost-5.7.25.tar.gz 
...
[root@localhost Downloads]# ls -l
drwxr-xr-x. 36 7161 31415      4096 12月 21 2018 mysql-5.7.25
-rw-rw-r--.  1 leo  leo    49107578 7月   8 19:48 mysql-boost-5.7.25.tar.gz
```

## 编译安装

`cmake` 配置项

```
-DCMAKE_INSTALL_PREFIX=/opt/mysql/5.7.25        # 安装目录 --basedir
-DMYSQL_DATADIR=/opt/mysql/5.7.25/data          # 数据目录 --datadir
-DSYSCONFDIR=/opt/mysql/5.7.25/etc             # my.cnf配置文件目录  --defaults-file
-DMYSQL_TCP_PORT=3306       # 端口号 --port
-DSYSTEMD_PID_DIR=/opt/mysql/5.7.25/mysqld.pid     # 当MySQL由systemd管理时，在其中创建PID文件的目录
-DMYSQL_UNIX_ADDR=/opt/mysql/5.7.25/mysql.sock     # 服务器在其上侦听套接字连接的Unix套接字文件路径 --socket
-DDEFAULT_CHARSET=utf8      # 服务器字符集 --character_set_server 
-DDEFAULT_COLLATION=utf8_general_ci     # 服务器排序规则 --collation_server
-DWITH_EXTRA_CHARSETS=all       # 包括的额外字符集
-DWITH_INNOBASE_STORAGE_ENGINE=1 
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 
-DWITH_ZLIB=bundled     # 使用压缩库支持构建
-DWITH_SSL=bundled      # 支持加密连接
-DENABLED_LOCAL_INFILE=1        # 控制本地MySQL客户端库的内置默认功能
-DWITH_EMBEDDED_SERVER=0        # 是否构建libmysqld嵌入式服务器库，MySQL 5.7.17开始不推荐使用嵌入式服务器库，并且已在MySQL 8.0中将其删除
-DENABLE_DOWNLOADS=1        # 是否下载可选文件
-DWITH_DEBUG=0              # 是否支持调试
-DWITH_BOOST=./boost/boost_1_59_0   # 指定Boost库目录位
-DWITH_SYSTEMD=1        # 是否启用安装systemd支持文件
```

`cmake` 配置

```
[root@localhost Downloads]# cd mysql-5.7.25
[root@localhost mysql-5.7.25]# mkdir bld && cd bld
[root@localhost bld]# cmake ../ \
-DCMAKE_INSTALL_PREFIX=/opt/mysql/5.7.25 \
-DMYSQL_DATADIR=/opt/mysql/5.7.25/data \
-DSYSCONFDIR=/opt/mysql/5.7.25/etc \
-DMYSQL_TCP_PORT=3306 \
-DSYSTEMD_PID_DIR=/opt/mysql/5.7.25/mysqld.pid \
-DMYSQL_UNIX_ADDR=/opt/mysql/5.7.25/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_EXTRA_CHARSETS=all \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
-DWITH_ZLIB=bundled \
-DWITH_SSL=bundled \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_EMBEDDED_SERVER=0 \
-DENABLE_DOWNLOADS=1 \
-DWITH_DEBUG=0 \
-DWITH_BOOST=../boost/boost_1_59_0 \
-DWITH_SYSTEMD=1
...
-- Configuring done
-- Generating done
-- Build files have been written to: /home/xxx/Downloads/mysql-5.7.25/bld
[root@localhost bld]# make && make install
...
```

## 配置文件 my.cnf

```
[root@localhost bld]# cd /opt/mysql/5.7.25/
[root@localhost 5.7.25]# mkdir etc
[root@localhost 5.7.25]# vim etc/my.cnf 
```

`my.cnf`

```bash
[mysqld]
port=3306
basedir=/opt/mysql/5.7.25
datadir=/opt/mysql/5.7.25/data
socket=/opt/mysql/5.7.25/mysql.sock
log-error=/opt/mysql/5.7.25/log/mysqld.log
pid-file=/opt/mysql/5.7.25/mysqld.pid
symbolic-links=0
max_allowed_packet=20M
default-time-zone = '+8:00'
bind_address='0.0.0.0'
character_set_server=utf8
collation_server=utf8_general_ci
autocommit=1
max_connections=1024
```

创建 `log` 目录

```
[root@localhost 5.7.25]# mkdir log
```

更改 安装目录的所属用户为 `mysql`

```
[root@localhost 5.7.25]# chown -R mysql:mysql /opt/mysql/5.7.25/
```

## 初始化数据目录

```
[root@localhost 5.7.25]# bin/mysqld --initialize --user=mysql
2020-07-08T14:00:35.171027Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2020-07-08T14:00:35.523723Z 0 [Warning] InnoDB: New log files created, LSN=45790
2020-07-08T14:00:35.596471Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2020-07-08T14:00:35.662833Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 6559e620-c123-11ea-aa1a-009b27e04c84.
2020-07-08T14:00:35.665818Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2020-07-08T14:00:35.667859Z 1 [Note] A temporary password is generated for root@localhost: R*udj_rdi3K&
```

## 启动数据库

一般启动方法

```
[root@localhost 5.7.25]# bin/mysqld --daemonize --user=mysql
```

`systemd` 管理

```
[root@localhost 5.7.25]# cp usr/lib/systemd/system/mysqld.service usr/lib/systemd/system/mysqld@.service /usr/lib/systemd/system/
[root@localhost 5.7.25]# vim /usr/lib/systemd/system/mysqld.service
```

修改 `mysqld.service`

```bash

#
# systemd service file for MySQL forking server
#

[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql

Type=forking

PIDFile=/opt/mysql/5.7.25/data/mysqld.pid

# Disable service start and stop timeout logic of systemd for mysqld service.
TimeoutSec=0

# Execute pre and post scripts as root
PermissionsStartOnly=true

# Needed to create system tables
ExecStartPre=/opt/mysql/5.7.25/bin/mysqld_pre_systemd

# Start main service
ExecStart=/opt/mysql/5.7.25/bin/mysqld --daemonize --pid-file=/opt/mysql/5.7.25/data/mysqld.pid $MYSQLD_OPTS

# Use this to switch malloc implementation
EnvironmentFile=-/etc/sysconfig/mysql

# Sets open_files_limit
LimitNOFILE = 5000

Restart=on-failure

RestartPreventExitStatus=1

PrivateTmp=false
```

重载服务配置

```
[root@localhost 5.7.25]# systemctl daemon-reload
```

开机自动启动

```
[root@localhost 5.7.25]# systemctl enable mysqld
```

启动服务

```
[root@localhost 5.7.25]# systemctl start mysqld
```

## 登录数据库修改密码

```
[root@localhost 5.7.25]# bin/mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.25

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

修改密码

```
mysql>ALTER USER 'root'@'localhost' IDENTIFIED BY 'ghJKJB&^!';
Query OK, 0 rows affected (0.00 sec)
```

忘记密码

```
# my.cnf 加入 skip-grant-tables ，启动

mysql>use mysql
mysql>update user set authentication_string = password('ghJKJB&^!') where user='root';

# my.cnf 去掉 skip-grant-tables ，重启

mysql>ALTER USER 'root'@'localhost' IDENTIFIED BY 'ghJKJB&^!';
Query OK, 0 rows affected (0.00 sec)
```

查看数据库

```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql>
```

## 以修改后的密码登录

```
[root@localhost 5.7.25]# bin/mysql -u root -p'ghJKJB&^!'  # 密码用引号引起来，-p后面不加空格
```

至此，`mysql` 安装完成。

## 配置环境变量 /etc/profile

```
export PATH=$PATH:/opt/mysql/5.7.25/bin
```

## 登录数据库

```
[root@localhost 5.7.25]# mysql -h 127.0.0.1 -P 3306 -u root -p'ghJKJB&^!'
```
