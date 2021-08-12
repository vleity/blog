# hadoop版本

hadoop-2.10.1

# 集群规划

| 主机名   | IP           | hdfs节点                 | yran节点 |
| -------- | ------------ | ------------------------ | -------- |
| hadoop01 | 192.168.146.101 | NameNode                 |          |
| hadoop02 | 192.168.146.102 | DataNode、SecondNameNode |          |
| hadoop03 | 192.168.146.103 | DataNode                 |          |


安装目录：/app

# 设置ip地址和主机名

```text
vim /etc/sysconfig/network-scripts/ifcfg-ens33
```

* 设置静态ip地址

```text
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static	# 静态ip
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=c2e067c0-7bd7-49ff-823e-a49323cfe1b6
DEVICE=ens33
ONBOOT=yes
IPADDR=192.168.146.101	# ip地址
NETMASK=255.255.255.0	# 子网掩码
GATEWAY=192.168.146.2	# 默认网关
DNS1=114.114.114.114
DNS2=8.8.8.8
```

* 修改主机名

```
echo hadoop01 > /etc/hostname
```

* 配置/etc/hosts

```
192.168.146.101 hadoop01
192.168.146.102 hadoop02
192.168.146.103 hadoop03
```

# 安装jdk环境

* 下载jdk：http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html#/

* 解压下载的压缩包到/app目录下

```text
tar -zxvf jdk-8u281-linux-x64.tar.gz -C /app/
```

* 设置java环境变量

```text
vim /etc/profile
```

```bash
export JAVA_HOME=/app/jdk1.8.0_281
export PATH=$PATH:$JAVA_HOME/bin
```

```text
source /etc/profile
```

* 查看java版本

```text
java -version

java version "1.8.0_281"
Java(TM) SE Runtime Environment (build 1.8.0_281-b09)
Java HotSpot(TM) 64-Bit Server VM (build 25.281-b09, mixed mode)
```

# 创建hadoop用户

```
useradd hadoop
```

在另外两台主机当中实现同样的操作，配置好主机

* ssh免密访问

```text
ssh-keygen
ssh-copy-id hadoop@hadoop01
ssh-copy-id hadoop@hadoop02
ssh-copy-id hadoop@hadoop03
```

# 安装Hadoop集群

* 下载hadoop安装包

```text
wget https://mirrors.bfsu.edu.cn/apache/hadoop/common/hadoop-2.10.1/hadoop-2.10.1.tar.gz
```

* 解压到/app

```text
tar -zxvf hadoop-2.10.1.tar.gz -C /app/
```

* 配置hadoop环境变量

```bash
export HADOOP_HOME=/app/hadoop-2.10.1
```

* 配置 hadoop-env.sh、mapred-env.sh、yarn-env.sh文件的JAVA_HOME参数

```bash
export JAVA_HOME=/app/jdk1.8.0_281
```

* 配置core-site.xml

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop01:9000</value>
  </property>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/app/hadoop-2.10.1/tmp</value>
  </property>
  <property>
    <name>hadoop.name.dir</name>
    <value>/app/hadoop-2.10.1/data/name</value>
  </property>
  <property>
    <name>hadoop.data.dir</name>
    <value>/app/hadoop-2.10.1/data/data</value>
  </property>
</configuration>
```

* 配置hdfs-site.xml

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
</configuration>
```
dfs.replication配置的是HDFS存储时的备份数量

* 配置mapred-site.xml(复制mapred-site.xml.template,再修改文件名)

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
```

* 配置yarn-site.xml

```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>hadoop01</value>
  </property>
</configuration>
```


* 同步hadoop包到两外两台主机

```text
rsync -rvl /app 
```

* 