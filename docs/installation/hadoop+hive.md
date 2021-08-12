下载安装包：

hadoop-2.7.7.tar.gz

apache-hive-2.3.8-bin.tar.gz



安装jdk并设置环境变量JAVA_HOME



解压hadoop

创建data/namenode目录

创建data/datanode目录

设置环境变量HADOOP_HOME，%HADOOP_HOME%\bin



修改配置文件etc/hadoop/hadoop-env.cmd

```text
set JAVA_HOME=E:\Java\jdk1.8.0_221
```

修改配置文件etc/hadoop/core-site.xml

```xml
<configuration>
<property>
      <name>fs.defaultFS</name>
      <value>hdfs://localhost:9000</value>
</property>
<property>
    <name>hadoop.tmp.dir</name>
    <value>/e:/bigdata/hadoop/data/</value>
</property>
</configuration>
```

修改配置文件etc/hadoop/mapred-site.xml

```xml
<configuration>
   <property>
       <name>mapreduce.framework.name</name>
       <value>yarn</value>
   </property>
</configuration>
```

修改配置文件etc/hadoop/hdfs-site.xml

```xml
<configuration>
<property>
       <name>dfs.replication</name>
       <value>1</value>
   </property>
   <property>
       <name>dfs.namenode.name.dir</name>
       <value>/e:/bigdata/hadoop/data/namenode</value>
   </property>
   <property>
       <name>dfs.datanode.data.dir</name>
     <value>/e:/bigdata/hadoop/data/datanode</value>
   </property>
</configuration>
```

修改配置文件etc/hadoop/yarn-site.xml

```xml
<configuration>
   <property>
       <name>yarn.nodemanager.aux-services</name>
       <value>mapreduce_shuffle</value>
   </property>
   <property>
       <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
       <value>org.apache.hadoop.mapred.ShuffleHandler</value>
   </property>
</configuration>
```

初始化namenode

```
bin\hadoop namenode -format
```

看到namenode has been successfully formatted.说明初始化成功，查看e:/bigdata/hadoop/data/namenode目录已经有内容了

启动hadoop，`sbin/start-all`





解压hive

设置环境变量HIVE_HOME，%HIVE_HOME%\bin

HIVE=HOME=E:\bigdata\apache-hive



配置文件

```text
hive-default.xml.template             ----->       hive-site.xml
hive-env.sh.template                     ----->             hive-env.sh
hive-exec-log4j.properties.template     ----->    hive-exec-log4j2.properties
hive-log4j.properties.template             ----->    hive-log4j2.properties
```

hadoop上创建hdfs目录

```text
hadoop fs -mkdir /tmp
hadoop fs -mkdir /user/
hadoop fs -mkdir /user/hive/
hadoop fs -mkdir /user/hive/warehouse 
hadoop fs -chmod g+w /tmp
hadoop fs -chmod g+w /user/hive/warehouse
```

hive-env.sh

```bash
# Set HADOOP_HOME to point to a specific hadoop install directory
export HADOOP_HOME=E:\bigdata\hadoop

# Hive Configuration Directory can be controlled by:
export HIVE_CONF_DIR=E:\bigdata\apache-hive\conf

# Folder containing extra libraries required for hive compilation/execution can be controlled by:
export HIVE_AUX_JARS_PATH=E:\bigdata\apache-hive\lib
```

hive-site.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?><!--
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
--><configuration>
  <!-- WARNING!!! This file is auto generated for documentation purposes ONLY! -->
  <!-- WARNING!!! Any changes you make to this file will be ignored by Hive.   -->
  <!-- WARNING!!! You must make your changes in hive-site.xml instead.         -->
  <!-- Hive Execution Parameters -->
<!--hive的临时数据目录，指定的位置在hdfs上的目录-->
	<property>
		<name>hive.metastore.warehouse.dir</name>
		<value>/user/hive/warehouse</value>
		<description>location of default database for the warehouse</description>
	</property>
 
 
 
<!--hive的临时数据目录，指定的位置在hdfs上的目录-->
	<property>
		<name>hive.exec.scratchdir</name>
		<value>/tmp/hive</value>
		<description>HDFS root scratch dir for Hive jobs which gets created with write all (733) permission. For each connecting user, an HDFS scratch dir: ${hive.exec.scratchdir}/&lt;username&gt; is created, with ${hive.scratch.dir.permission}.</description>
	</property>
 
 
 
<!-- scratchdir 本地目录 -->
	<property>
		<name>hive.exec.local.scratchdir</name>
		<value>E:/bigdata/apache-hive/local/scratch</value>
		<description>Local scratch space for Hive jobs</description>
	</property>
 
<!-- resources_dir 本地目录 -->
	<property>
		<name>hive.downloaded.resources.dir</name>
		<value>E:/bigdata/apache-hive/local/resources/${hive.session.id}_resources</value>
		<description>Temporary local directory for added resources in the remote file system.</description>
	</property>
 
<!-- querylog 本地目录 -->
	<property>
		<name>hive.querylog.location</name>
		<value>E:/bigdata/apache-hive/local/querylog</value>
		<description>Location of Hive run time structured log file</description>
	</property>
 
<!-- operation_logs 本地目录 -->
	<property>
		<name>hive.server2.logging.operation.log.location</name>
		<value>E:/bigdata/apache-hive/local/operation_logs</value>
		<description>Top level directory where operation logs are stored if logging functionality is enabled</description>
	</property>
 
<!-- 数据库连接地址配置 -->
	<property>
		<name>javax.jdo.option.ConnectionURL</name>
		<value>jdbc:postgresql://localhost:5432/hive?createDatabaseIfNotExist=true</value>
		<description>
		JDBC connect string for a JDBC metastore.
		</description>
	</property>
 
<!-- 数据库驱动配置 -->
	<property>
		<name>javax.jdo.option.ConnectionDriverName</name>
		<value>org.postgresql.Driver</value>
		<description>Driver class name for a JDBC metastore</description>
	</property>
 
<!-- 数据库用户名 -->
	<property>
		<name>javax.jdo.option.ConnectionUserName</name>
		<value>hive</value>
		<description>Username to use against metastore database</description>
	</property>
 
<!-- 数据库访问密码 -->
	<property>
		<name>javax.jdo.option.ConnectionPassword</name>
		<value>hive</value>
		<description>password to use against metastore database</description>
	</property>
 
<!-- 解决 Caused by: MetaException(message:Version information not found in metastore. ) -->
	<property>
		<name>hive.metastore.schema.verification</name>
		<value>false</value>
		<description>
		Enforce metastore schema version consistency.
		True: Verify that version information stored in is compatible with one from Hive jars. Also disable automatic
		schema migration attempt. Users are required to manually migrate schema after Hive upgrade which ensures
		proper metastore schema migration. (Default)
		False: Warn if the version information stored in metastore doesn't match with one from in Hive jars.
		</description>
	</property>
 
<!-- 自动创建全部 -->
<!-- hive Required table missing : "DBS" in Catalog""Schema" 错误 -->
	<property>
		<name>datanucleus.schema.autoCreateAll</name>
		<value>true</value>
		<description>Auto creates necessary schema on a startup if one doesn't exist. Set this to false, after creating it once.To enable auto create also set hive.metastore.schema.verification=false. Auto creation is not recommended for production use cases, run schematool command instead.</description>
	</property>
</configuration>
```

创建hive用户，hive数据库



```
create user hive password 'hive';
create database hive owner hive;

create schema hive authorization hive;
```



Hive 初始化数据，执行指令：

```
hive --service metastore
```



































