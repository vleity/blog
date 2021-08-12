## 创建数据库的语句

可以通过 \h 来查看创建数据库的语句

```text
mysql> \h create database
Name: 'CREATE DATABASE'
Description:
Syntax:
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name

CREATE DATABASE creates a database with the given name. To use this
statement, you need the CREATE privilege for the database. CREATE
SCHEMA is a synonym for CREATE DATABASE.

URL: http://dev.mysql.com/doc/refman/5.7/en/create-database.html

```

`show character set` 查看有哪些字符集

`show collation` 查看有哪些排序规则


创建一个数据库，编码为 `utf8 `,排序规则编码为 `utf8_general_ci`

```text
mysql> create database test default character set utf8 default collate utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| leity              |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
6 rows in set (0.00 sec)
```

## 删除数据库

`drop database 数据库名`


## 创建用户

`create user 用户 identified by '密码';`

```text
mysql> create user user1 identified by '12345';  --用户可在任何host（%）登录
Query OK, 0 rows affected (0.00 sec)

mysql> select host,user from user;
+-----------+---------------+
| host      | user          |
+-----------+---------------+
| %         | root          |
| %         | user1         |
| localhost | mysql.session |
| localhost | mysql.sys     |
| localhost | root          |
+-----------+---------------+
5 rows in set (0.00 sec)

```
- 创建只能在固定 host 登录的用户

`create user 用户@'192.168.0.1' identified by '密码';`

```text
mysql> create user user2@'192.168.0.1' identified by '12345';
Query OK, 0 rows affected (0.00 sec)

mysql> select host,user from user;
+-------------+---------------+
| host        | user          |
+-------------+---------------+
| %           | root          |
| %           | user1         |
| 192.168.0.1 | user2         |
| localhost   | mysql.session |
| localhost   | mysql.sys     |
| localhost   | root          |
+-------------+---------------+
6 rows in set (0.00 sec)

```

## 删除用户

**默认删除的是`用户@'%'`的指令**

```text
mysql> drop user user2;
ERROR 1396 (HY000): Operation DROP USER failed for 'user2'@'%'
mysql> drop user user2@'192.168.0.1';
Query OK, 0 rows affected (0.00 sec)
mysql> drop user user1;
Query OK, 0 rows affected (0.00 sec)
```

## 设置访问权限

`user2` 登录，查看拥有的权限

```text
mysql> show grants;
+-------------------------------------------+
| Grants for user2@localhost                |
+-------------------------------------------+
| GRANT USAGE ON *.* TO 'user2'@'localhost' |
+-------------------------------------------+
1 row in set (0.00 sec)

```

管理员用户对 `user2` 授予在 `test` 库的 `select` 权限

```text
mysql> grant select on test.* to user2@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> 

```

`user2` 登录，查看拥有的权限

```text
mysql> show grants;
+-------------------------------------------------+
| Grants for user2@localhost                      |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'user2'@'localhost'       |
| GRANT SELECT ON `test`.* TO 'user2'@'localhost' |
+-------------------------------------------------+
2 rows in set (0.00 sec)

```

收回权限

```text
revoke select on test.* from user2@'localhost';
```

## 修改密码

```text
mysql> set password for user2@'localhost' = Password('123');
Query OK, 0 rows affected, 1 warning (0.00 sec)

```

也可以直接更新 `mysql` 库的 `user` 表，密码要用 `password` 函数加密，注意看存储密码的字段是哪一个，字段名不一定叫 `password`

```text
update user set password = password('123') where user = 'user2' and host='localhost';
```


## 查看数据库和表

- show databases 查看数据库

```text
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| leity              |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)
mysql> 
```

- show tables 查看表

```text
mysql> show tables;
+---------------------------+
| Tables_in_mysql           |
+---------------------------+
| columns_priv              |
| db                        |
...
| user                      |
+---------------------------+
31 rows in set (0.00 sec)

mysql> 
```

- show columns from 表名 或 desc 表名

```text
mysql> show columns from user;
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
| Field                  | Type                              | Null | Key | Default               | Extra |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
| Host                   | char(60)                          | NO   | PRI |                       |       |
| User                   | char(32)                          | NO   | PRI |                       |       |
...
| account_locked         | enum('N','Y')                     | NO   |     | N                     |       |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
45 rows in set (0.00 sec)

mysql>
```

- show status 查看数据库的状态

```text
mysql> show status;
+-----------------------------------------------+--------------------------------------------------+
| Variable_name                                 | Value                                            |
+-----------------------------------------------+--------------------------------------------------+
| Aborted_clients                               | 0                                                |
| Aborted_connects                              | 0                                                |
...
```

- show grants 查看当前用户的权限

```text
mysql> show grants;
+---------------------------------------------------------------------+
| Grants for root@localhost                                           |
+---------------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION |
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION        |
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)

```

- show errors / warings 查看

## 查看 show 的用法，使用 \h

```text
mysql> \h show
Name: 'SHOW'
Description:
SHOW has many forms that provide information about databases, tables,
columns, or status information about the server. This section describes
those following:

SHOW {BINARY | MASTER} LOGS
SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW CHARACTER SET [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE DATABASE db_name
SHOW CREATE EVENT event_name
SHOW CREATE FUNCTION func_name
SHOW CREATE PROCEDURE proc_name
SHOW CREATE TABLE tbl_name
SHOW CREATE TRIGGER trigger_name
SHOW CREATE VIEW view_name
SHOW DATABASES [like_or_where]
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW ERRORS [LIMIT [offset,] row_count]
SHOW EVENTS
SHOW FUNCTION CODE func_name
SHOW FUNCTION STATUS [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
SHOW MASTER STATUS
SHOW OPEN TABLES [FROM db_name] [like_or_where]
SHOW PLUGINS
SHOW PROCEDURE CODE proc_name
SHOW PROCEDURE STATUS [like_or_where]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW PROFILE [types] [FOR QUERY n] [OFFSET n] [LIMIT n]
SHOW PROFILES
SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW SLAVE HOSTS
SHOW SLAVE STATUS [FOR CHANNEL channel]
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS [LIMIT [offset,] row_count]

like_or_where:
    LIKE 'pattern'
  | WHERE expr

If the syntax for a given SHOW statement includes a LIKE 'pattern'
part, 'pattern' is a string that can contain the SQL % and _ wildcard
characters. The pattern is useful for restricting statement output to
matching values.

Several SHOW statements also accept a WHERE clause that provides more
flexibility in specifying which rows to display. See
http://dev.mysql.com/doc/refman/5.7/en/extended-show.html.

URL: http://dev.mysql.com/doc/refman/5.7/en/show.html

```












