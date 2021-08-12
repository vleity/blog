#### 安装依赖

```shell
yum install -y gcc gcc-c++ make readline readline-devel perl perl-devel perl-ExtUtils-Embed systemd systemd-devel tcl tcl-devel
```

#### 下载源码

```shell
wget http://mirrors.ustc.edu.cn/postgresql/source/v12.2/postgresql-12.2.tar.gz
```

#### 解压

```shell
tar -zxvf postgresql-12.2.tar.gz
cd postgresql-12.2
```

#### 编译安装【root】

```shell
[root@orig_02 postgresql-12.2]# export PYTHON='python3'
[root@orig_02 postgresql-12.2]# ./configure --prefix=/opt/postgresql/12.2 --with-perl --with-python --with-tcl --with-openssl --with-systemd
[root@orig_02 postgresql-12.2]# make world && make install-world
```

#### 进入安装后的目录，常见data和log目录

```shell
[root@orig_02 postgresql-12.2]# cd /opt/postgresql/12.2/
[root@orig_02 12.2]# mkdir data
[root@orig_02 12.2]# mkdir log
```

#### 创建postgres用户

```shell
[root@orig_02 12.2]# useradd postgres
[root@orig_02 12.2]# passwd postgres
Changing password for user postgres.
New password: 
BAD PASSWORD: The password contains the user name in some form
Retype new password: 
passwd: all authentication tokens updated successfully.
```

#### 切换目录所有者

```shell
[root@orig_02 12.2]# chown -R postgres:root /opt/postgresql/
```

#### 初始化数据库【postgres】

```shell
[postgres@orig_02 ~]$ /opt/postgresql/12.2/bin/initdb -D /opt/postgresql/12.2/data/
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.UTF-8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /opt/postgresql/12.2/data ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... Asia/Shanghai
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok

initdb: warning: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.

Success. You can now start the database server using:

    /opt/postgresql/12.2/bin/pg_ctl -D /opt/postgresql/12.2/data/ -l logfile start
```

#### 设置环境变量

```shell
[postgres@orig_02 data]$ vim ~/.bash_profile
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

# postgresql

PGHOME=/opt/postgresql/12.2
PGDATA=/opt/postgresql/12.2/data

PATH=$PATH:$HOME/.local/bin:$HOME/bin:$PGHOME/bin

export PATH

[postgres@orig_02 data]$ source ~/.bash_profile
```

#### 编辑配置文件

```shell
[postgres@orig_02 data]$ vim /opt/postgresql/12.2/data/postgresql.conf
listen_addresses = '*'
port = 5432


[postgres@orig_02 data]$ vim /opt/postgresql/12.2/data/pg_hba.conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             0.0.0.0/0               md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     md5
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5

```

#### 启动数据库

```shell
[postgres@orig_02 data]$ pg_ctl -D /opt/postgresql/12.2/data -l /opt/postgresql/12.2/log/pg.log start
```

#### 开放端口

```shell
[root@orig_02 12.2]# firewall-cmd --zone=public --add-port=5432/tcp --permanent
success
[root@orig_02 12.2]# firewall-cmd --reload
success
```

#### 关闭数据库

```shell
[postgres@orig_02 data]$ pg_ctl -D /opt/postgresql/12.2/data -l /opt/postgresql/12.2/log/pg.log stop
```

#### 连接数据库

```shell
[postgres@orig_02 data]$ psql -h 127.0.0.1 -p 5432 -U postgres -W -d postgres
```

