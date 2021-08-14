# postgresql

# 一、psql连接数据库

一般用法

```sql
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -W
--多主机
psql -h 132.108.212.128,132.121.1.74 -p 5433,5553 -U bss_gz -d jsdb
```

字符串的形式，字符串放在最后面，psql操作选项要在字符串前

```sql
psql "host=132.108.212.128 port=5433 dbname=jsdb user=bss_gz password=ZuseP*NFye86"
--多h主机 host=host1,host2 port=port1,port2
psql "host=132.108.212.128,132.121.1.74 port=5433,5553 dbname=test user=test password=Zugsdbsvaf86"
```

URI用法：

`postgresql://[user[:password]@][netloc][:port][,...][/dbname][?param1=value1&...]`

`postgres://[user[:password]@][netloc][:port][,...][/dbname][?param1=value1&...]`

参考 [34.1. 数据库连接控制函数](http://postgres.cn/docs/11/libpq-connect.html)

```sql
--psql postgresql://{user}:{password}@{host}:{port}/{dbname}
psql postgresql://test:Zugsdbsvaf86@132.108.212.128:5433/test
--多主机 host1:port1,host2:port2
psql postgresql://bss_gz:Zugsdbsvaf86@132.108.212.128:5433,132.121.1.74:5553/test
```

使用service文件

```sql
psql service=cn
```

```sql
# CN节点
[cn]
host=132.108.212.128
port=5433
dbname=test
user=test
password=Zugsdbsvaf86
keepalives_idle=60	# 连接保持
```

多主机，host 之间用逗号跟开，port 之间用逗号隔开，host 与 port 一一对应

```sql
# worker节点
[worker]
host=132.121.1.69,132.121.1.70
port=5463,5493
dbname=test
user=test
password=Zugsdbsvaf86
keepalives_idle=60	# 连接保持
connect_timeout=2
```



`keepalives_idle=60`  保持连接

# 二、创建数据库

```
postgres=# create user orig with password '123456';
postgres=# create database orig with owner orig;
postgres=# \c orig
orig=# drop schema public;
orig=# create schema orig authorization orig;
orig=# set search_path="$user";
orig=# show search_path;
 search_path
-------------
 "$user"
(1 行记录)
```

# 三、列出数据库

```
postgres=# \l
                                                        数据库列表
   名称    |  拥有者  | 字元编码 |            校对规则            |             Ctype              |       存取权限
-----------+----------+----------+--------------------------------+--------------------------------+-----------------------
 orig      | postgres | UTF8     | Chinese (Simplified)_China.936 | Chinese (Simplified)_China.936 |
 postgres  | postgres | UTF8     | Chinese (Simplified)_China.936 | Chinese (Simplified)_China.936 |
 template0 | postgres | UTF8     | Chinese (Simplified)_China.936 | Chinese (Simplified)_China.936 | =c/postgres          +
           |          |          |                                |                                | postgres=CTc/postgres
 template1 | postgres | UTF8     | Chinese (Simplified)_China.936 | Chinese (Simplified)_China.936 | =c/postgres          +
           |          |          |                                |                                | postgres=CTc/postgres
(4 行记录)
```

# 四、切换数据库

`\c + 数据库名`

`psql -h 127.0.0.1 -p 5432 -U postgres -W -d orig`

```
postgres=# \c orig
用户 postgres 的口令：
您现在已经连接到数据库 "orig",用户 "postgres".
orig=#
```

# 五、删除数据库

`DROP DATABASE orig`

```
orig=# drop database orig;
错误:  无法删除当前使用的数据库
\c postgres
用户 postgres 的口令：
您现在已经连接到数据库 "postgres",用户 "postgres".
postgres=# drop database orig;
DROP DATABASE
postgres=#
```

# 六、创建表

```sql
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);
```

查看表

```
postgres=# \d
                 关联列表
 架构模式 |    名称    |  类型  |  拥有者
----------+------------+--------+----------
 public   | company    | 数据表 | postgres
 public   | department | 数据表 | postgres
(2 行记录)


postgres=# \d company
                 数据表 "public.company"
  栏位   |     类型      | Collation | Nullable | Default
---------+---------------+-----------+----------+---------
 id      | integer       |           | not null |
 name    | text          |           | not null |
 age     | integer       |           | not null |
 address | character(50) |           |          |
 salary  | real          |           |          |
索引：
    "company_pkey" PRIMARY KEY, btree (id)
```

# 七、insert多行

```sql
INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE) 
VALUES 
(4, 'Mark', 25, 'Rich-Mond ', 65000.00, '2007-12-13' ), 
(5, 'David', 27, 'Texas', 85000.00, '2007-12-13')
```

# 八、运算符

假设变量 a 为 2，变量 b 为 3，则：

| 运算符 |        描述        |        实例         |
| :----: | :----------------: | :-----------------: |
|   +    |         加         |   a + b 结果为 5    |
|   -    |         减         |   a - b 结果为 -1   |
|   *    |         乘         |   a * b 结果为 6    |
|   /    |         除         |   b / a 结果为 1    |
|   %    |     模（取余）     |   b % a 结果为 1    |
|   ^    |        指数        |   a ^ b 结果为 8    |
|  \|/   |       平方根       |  \|/ 25.0 结果为 5  |
| \|\|/  |       立方根       | \|\|/ 27.0 结果为 3 |
|   !    |        阶乘        |   5 ! 结果为 120    |
|   !!   | 阶乘（前缀操作符） |   !! 5 结果为 120   |

```
postgres=# select 1+1;
 ?column?
----------
        2
(1 行记录)


postgres=# select 2-1;
 ?column?
----------
        1
(1 行记录)


postgres=# select 2*3;
 ?column?
----------
        6
(1 行记录)


postgres=# select 3/2;
 ?column?
----------
        1
(1 行记录)


postgres=# select 3%2;
 ?column?
----------
        1
(1 行记录)


postgres=# select 2^3;
 ?column?
----------
        8
(1 行记录)


postgres=# select |/16;
 ?column?
----------
        4
(1 行记录)


postgres=# select ||/27;
 ?column?
----------
        3
(1 行记录)


postgres=# select 5!;
 ?column?
----------
      120
(1 行记录)


postgres=# select !!5;
 ?column?
----------
      120
(1 行记录)
```

# 九、时间

```
SELECT CURRENT_TIMESTAMP;
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;
```

# 十、limit

```SQL
--读取 4 条数据：
SELECT * FROM COMPANY LIMIT 4;

--从第三位开始提取 3 个记录
SELECT * FROM COMPANY LIMIT 3 OFFSET 2;
```

# 十一、copy导入导出数据

```sql
CREATE TABLE table_report (
	job_name VARCHAR ( 64 ),
	TABLE_NAME VARCHAR ( 64 ),
	PROV_CODE VARCHAR ( 64 ),
	JOB_START_TIME VARCHAR ( 20 ),
	JOB_END_TIME VARCHAR ( 20 ),
	ALL_OF_DATA VARCHAR ( 64 ),
	NUMBER_OF_DATA VARCHAR ( 64 ) 
);

# 导入
orig=# copy table_report from 'E:\Auto_process\hana_table_report\table_report.txt' with csv;
COPY 583

# 导出
orig=# copy table_report to 'E:\Auto_process\hana_table_report\table_report.csv' with csv;
COPY 583

```

# 十二、数据类型

| 名字                                        | 别名                     | 描述                                          |
| ------------------------------------------- | ------------------------ | --------------------------------------------- |
| `bigint`                                    | `int8`                   | 有符号的8字节整数                             |
| `bigserial`                                 | `serial8`                | 自动增长的8字节整数                           |
| `bit [ (*n*) ]`                             |                          | 定长位串                                      |
| `bit varying [ (*n*) ]`                     | `varbit`                 | 变长位串                                      |
| `boolean`                                   | `bool`                   | 逻辑布尔值（真/假）                           |
| `box`                                       |                          | 平面上的普通方框                              |
| `bytea`                                     |                          | 二进制数据（“字节数组”）                      |
| `character [ (*n*) ]`                       | `char [ (*n*) ]`         | 定长字符串                                    |
| `character varying [ (*n*) ]`               | `varchar [ (*n*) ]`      | 变长字符串                                    |
| `cidr`                                      |                          | IPv4或IPv6网络地址                            |
| `circle`                                    |                          | 平面上的圆                                    |
| `date`                                      |                          | 日历日期（年、月、日）                        |
| `double precision`                          | `float8`                 | 双精度浮点数（8字节）                         |
| `inet`                                      |                          | IPv4或IPv6主机地址                            |
| `integer`                                   | `int`, `int4`            | 有符号4字节整数                               |
| `interval [ *fields* ] [ (*p*) ]`           |                          | 时间段                                        |
| `json`                                      |                          | 文本 JSON 数据                                |
| `jsonb`                                     |                          | 二进制 JSON 数据，已分解                      |
| `line`                                      |                          | 平面上的无限长的线                            |
| `lseg`                                      |                          | 平面上的线段                                  |
| `macaddr`                                   |                          | MAC（Media Access Control）地址               |
| `macaddr8`                                  |                          | MAC (Media Access Control) 地址 (EUI-64 格式) |
| `money`                                     |                          | 货币数量                                      |
| `numeric [ (*p*, *s*) ]`                    | `decimal [ (*p*, *s*) ]` | 可选择精度的精确数字                          |
| `path`                                      |                          | 平面上的几何路径                              |
| `pg_lsn`                                    |                          | PostgreSQL日志序列号                          |
| `point`                                     |                          | 平面上的几何点                                |
| `polygon`                                   |                          | 平面上的封闭几何路径                          |
| `real`                                      | `float4`                 | 单精度浮点数（4字节）                         |
| `smallint`                                  | `int2`                   | 有符号2字节整数                               |
| `smallserial`                               | `serial2`                | 自动增长的2字节整数                           |
| `serial`                                    | `serial4`                | 自动增长的4字节整数                           |
| `text`                                      |                          | 变长字符串                                    |
| `time [ (*p*) ] [ without time zone ]`      |                          | 一天中的时间（无时区）                        |
| `time [ (*p*) ] with time zone`             | `timetz`                 | 一天中的时间，包括时区                        |
| `timestamp [ (*p*) ] [ without time zone ]` |                          | 日期和时间（无时区）                          |
| `timestamp [ (*p*) ] with time zone`        | `timestamptz`            | 日期和时间，包括时区                          |
| `tsquery`                                   |                          | 文本搜索查询                                  |
| `tsvector`                                  |                          | 文本搜索文档                                  |
| `txid_snapshot`                             |                          | 用户级别事务ID快照                            |
| `uuid`                                      |                          | 通用唯一标识码                                |
| `xml`                                       |                          | XML数据                                       |

## 数值型

一般：

整数：integer，bigint

小数：numeric，decimal

序列：特殊的整数

```SQL
--序列使用，实际是创建了一个序列，id默认值为 nextval('serial_table_id_seq'::regclass)
create table serial_table
(
  id serial,
	name varchar(100)
);

insert into serial_table(name) values
('A'),('B'),('C'),('D'),('E'),('F'),('G');

SELECT * FROM serial_table;
orig=# SELECT * FROM serial_table;
 id | name
----+------
  1 | A
  2 | A
  3 | B
  4 | C
  5 | D
  6 | E
  7 | F
  8 | G
```



| 名字               | 存储尺寸 | 描述               | 范围                                         |
| ------------------ | -------- | ------------------ | -------------------------------------------- |
| `smallint`         | 2字节    | 小范围整数         | -32768 to +32767                             |
| `integer`          | 4字节    | 整数的典型选择     | -2147483648 to +2147483647                   |
| `bigint`           | 8字节    | 大范围整数         | -9223372036854775808 to +9223372036854775807 |
| `decimal`          | 可变     | 用户指定精度，精确 | 最高小数点前131072位，以及小数点后16383位    |
| `numeric`          | 可变     | 用户指定精度，精确 | 最高小数点前131072位，以及小数点后16383位    |
| `real`             | 4字节    | 可变精度，不精确   | 6位十进制精度                                |
| `double precision` | 8字节    | 可变精度，不精确   | 15位十进制精度                               |
| `smallserial`      | 2字节    | 自动增加的小整数   | 1到32767                                     |
| `serial`           | 4字节    | 自动增加的整数     | 1到2147483647                                |
| `bigserial`        | 8字节    | 自动增长的大整数   | 1到9223372036854775807                       |

## 货币类型

| 名字    | 存储尺寸 | 描述   | 范围                                         |
| ------- | -------- | ------ | -------------------------------------------- |
| `money` | 8 bytes  | 货币额 | -92233720368547758.08到+92233720368547758.07 |

## 字符类型

别名：varchar(n)，char(n)

text

| 名字                                     | 描述           |
| ---------------------------------------- | -------------- |
| `character varying(*n*)`, `varchar(*n*)` | 有限制的变长   |
| `character(*n*)`, `char(*n*)`            | 定长，空格填充 |
| `text`                                   | 无限变长       |

## 二进制数据类型

| 名字    | 存储尺寸                   | 描述         |
| ------- | -------------------------- | ------------ |
| `bytea` | 1或4字节外加真正的二进制串 | 变长二进制串 |

## 日期时间类型

timestamp <==> timestamp without time zone

timestamptz <==> timestamp with time zone

| 名字                                        | 存储尺寸 | 描述                               | 最小值        | 最大值        | 解析度       |
| ------------------------------------------- | -------- | ---------------------------------- | ------------- | ------------- | ------------ |
| `timestamp [ (*p*) ] [ without time zone ]` | 8字节    | 包括日期和时间（无时区）           | 4713 BC       | 294276 AD     | 1微秒 / 14位 |
| `timestamp [ (*p*) ] with time zone`        | 8字节    | 包括日期和时间，有时区             | 4713 BC       | 294276 AD     | 1微秒 / 14位 |
| `date`                                      | 4字节    | 日期（没有一天中的时间）           | 4713 BC       | 5874897 AD    | 1日          |
| `time [ (*p*) ] [ without time zone ]`      | 8字节    | 一天中的时间（无日期）             | 00:00:00      | 24:00:00      | 1微秒 / 14位 |
| `time [ (*p*) ] with time zone`             | 12字节   | 一天中的时间（不带日期），带有时区 | 00:00:00+1459 | 24:00:00-1459 | 1微秒 / 14位 |
| `interval [ *fields* ] [ (*p*) ]`           | 16字节   | 时间间隔                           | -178000000年  | 178000000年   | 1微秒 / 14位 |

## 布尔类型

| 名字      | 存储字节 | 描述         |
| --------- | -------- | ------------ |
| `boolean` | 1字节    | 状态为真或假 |

## 枚举类型

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

## 几何类型

| 名字      | 存储尺寸   | 表示                     | 描述                                |
| --------- | ---------- | ------------------------ | ----------------------------------- |
| `point`   | 16字节     | 平面上的点               | (x,y)                               |
| `line`    | 32字节     | 无限长的线               | {A,B,C}                             |
| `lseg`    | 32字节     | 有限线段                 | ((x1,y1),(x2,y2))                   |
| `box`     | 32字节     | 矩形框                   | ((x1,y1),(x2,y2))                   |
| `path`    | 16+16n字节 | 封闭路径（类似于多边形） | ((x1,y1),...)                       |
| `path`    | 16+16n字节 | 开放路径                 | [(x1,y1),...]                       |
| `polygon` | 40+16n字节 | 多边形（类似于封闭路径） | ((x1,y1),...)                       |
| `circle`  | 24字节     | 圆                       | <(x,y),r> (center point and radius) |

# 十三、时间字符串转换

| **函数**                        | **返回类型** | **描述**                  | **例子**                                                   |
| ------------------------------- | ------------ | ------------------------- | ---------------------------------------------------------- |
| to_char(timestamp, text)        | text         | 把时间戳转换成字串        | to_char(current_timestamp, 'HH12:MI:SS')                   |
| to_char(interval, text)         | text         | 把时间间隔转为字串        | to_char(interval '15h 2m 12s', 'HH24:MI:SS')               |
| to_char(int, text)              | text         | 把整数转换成字串          | to_char(125, '999')                                        |
| to_char(double precision, text) | text         | 把实数/双精度数转换成字串 | to_char(125.8::real, '999D9')                              |
| to_char(numeric, text)          | text         | 把numeric转换成字串       | to_char(-125.8, '999D99S')                                 |
| to_date(text, text)             | date         | 把字串转换成日期          | to_date('05 Dec 2000', 'DD Mon YYYY')                      |
| to_timestamp(text, text)        | timestamp    | 把字串转换成时间戳        | to_timestamp('05 Dec 2000', 'DD Mon YYYY')                 |
| to_timestamp(double)            | timestamp    | 把UNIX纪元转换成时间戳    | to_timestamp(200120400)                                    |
| extract(field from timestamp)   | double       | 获取UNIX纪元时间          | extract (epoch from timestamptz '1970-01-01 08:00:00+08'); |
| to_number(text, text)           | numeric      | 把字串转换成numeric       | to_number('12,454.8-', '99G999D9S')                        |

 

| **模式** | **描述**                                     |
| -------- | -------------------------------------------- |
| HH       | 一天的小时数(01-12)                          |
| HH12     | 一天的小时数(01-12)                          |
| HH24     | 一天的小时数(00-23)                          |
| MI       | 分钟(00-59)                                  |
| SS       | 秒(00-59)                                    |
| MS       | 毫秒(000-999)                                |
| US       | 微秒(000000-999999)                          |
| AM       | 正午标识(大写)                               |
| Y,YYY    | 带逗号的年(4和更多位)                        |
| YYYY     | 年(4和更多位)                                |
| YYY      | 年的后三位                                   |
| YY       | 年的后两位                                   |
| Y        | 年的最后一位                                 |
| MONTH    | 全长大写月份名(空白填充为9字符)              |
| Month    | 全长混合大小写月份名(空白填充为9字符)        |
| month    | 全长小写月份名(空白填充为9字符)              |
| MON      | 大写缩写月份名(3字符)                        |
| Mon      | 缩写混合大小写月份名(3字符)                  |
| mon      | 小写缩写月份名(3字符)                        |
| MM       | 月份号(01-12)                                |
| DAY      | 全长大写日期名(空白填充为9字符)              |
| Day      | 全长混合大小写日期名(空白填充为9字符)        |
| day      | 全长小写日期名(空白填充为9字符)              |
| DY       | 缩写大写日期名(3字符)                        |
| Dy       | 缩写混合大小写日期名(3字符)                  |
| dy       | 缩写小写日期名(3字符)                        |
| DDD      | 一年里的日子(001-366)                        |
| DD       | 一个月里的日子(01-31)                        |
| D        | 一周里的日子(1-7；周日是1)                   |
| W        | 一个月里的周数(1-5)(第一周从该月第一天开始)  |
| WW       | 一年里的周数(1-53)(第一周从该年的第一天开始) |

| **模式** | **描述**                         |
| -------- | -------------------------------- |
| 9        | 带有指定数值位数的值             |
| 0        | 带前导零的值                     |
| .(句点)  | 小数点                           |
| ,(逗号)  | 分组(千)分隔符                   |
| PR       | 尖括号内负值                     |
| S        | 带符号的数值                     |
| L        | 货币符号                         |
| D        | 小数点                           |
| G        | 分组分隔符                       |
| MI       | 在指明的位置的负号(如果数字 < 0) |
| PL       | 在指明的位置的正号(如果数字 > 0) |
| SG       | 在指明的位置的正/负号            |

| **操作符** | **例子**                                                    | **结果**                     |
| ---------- | ----------------------------------------------------------- | ---------------------------- |
| +          | date '2001-09-28' + integer '7'                             | date '2001-10-05'            |
| +          | date '2001-09-28' + interval '1 hour'                       | timestamp '2001-09-28 01:00' |
| +          | date '2001-09-28' + time '03:00'                            | timestamp '2001-09-28 03:00' |
| +          | interval '1 day' + interval '1 hour'                        | interval '1 day 01:00'       |
| +          | timestamp '2001-09-28 01:00' + interval '23 hours'          | timestamp '2001-09-29 00:00' |
| +          | time '01:00' + interval '3 hours'                           | time '04:00'                 |
| -          | - interval '23 hours'                                       | interval '-23:00'            |
| -          | date '2001-10-01' - date '2001-09-28'                       | integer '3'                  |
| -          | date '2001-10-01' - integer '7'                             | date '2001-09-24'            |
| -          | date '2001-09-28' - interval '1 hour'                       | timestamp '2001-09-27 23:00' |
| -          | time '05:00' - time '03:00'                                 | interval '02:00'             |
| -          | time '05:00' - interval '2 hours'                           | time '03:00'                 |
| -          | timestamp '2001-09-28 23:00' - interval '23 hours'          | timestamp '2001-09-28 00:00' |
| -          | interval '1 day' - interval '1 hour'                        | interval '23:00'             |
| -          | timestamp '2001-09-29 03:00' - timestamp '2001-09-27 12:00' | interval '1 day 15:00'       |
| *          | interval '1 hour' * double precision '3.5'                  | interval '03:30'             |
| /          | interval '1 hour' / double precision '1.5'                  | interval '00:40'             |

| **函数**                      | **返回类型** | **描述**                                     | **例子**                                            | **结果**                |
| ----------------------------- | ------------ | -------------------------------------------- | --------------------------------------------------- | ----------------------- |
| age(timestamp, timestamp)     | interval     | 减去参数，生成一个使用年、月的"符号化"的结果 | age('2001-04-10', timestamp '1957-06-13')           | 43 years 9 mons 27 days |
| age(timestamp)                | interval     | 从current_date减去得到的数值                 | age(timestamp '1957-06-13')                         | 43 years 8 mons 3 days  |
| current_date                  | date         | 今天的日期                                   |                                                     |                         |
| current_time                  | time         | 现在的时间                                   |                                                     |                         |
| current_timestamp             | timestamp    | 日期和时间                                   |                                                     |                         |
| date_part(text, timestamp)    | double       | 获取子域(等效于extract)                      | date_part('hour', timestamp '2001-02-16 20:38:40')  | 20                      |
| date_part(text, interval)     | double       | 获取子域(等效于extract)                      | date_part('month', interval '2 years 3 months')     | 3                       |
| date_trunc(text, timestamp)   | timestamp    | 截断成指定的精度                             | date_trunc('hour', timestamp '2001-02-16 20:38:40') | 2001-02-16 20:00:00+00  |
| extract(field from timestamp) | double       | 获取子域                                     | extract(hour from timestamp '2001-02-16 20:38:40')  | 20                      |
| extract(field from interval)  | double       | 获取子域                                     | extract(month from interval '2 years 3 months')     | 3                       |
| localtime                     | time         | 今日的时间                                   |                                                     |                         |
| localtimestamp                | timestamp    | 日期和时间                                   |                                                     |                         |
| now()                         | timestamp    | 当前的日期和时间(等效于 current_timestamp)   |                                                     |                         |
| timeofday()                   | text         | 当前日期和时间                               |                                                     |                         |

| **域**       | **描述**                                                     | **例子**                                                  | **结果** |
| ------------ | ------------------------------------------------------------ | --------------------------------------------------------- | -------- |
| CENTURY      | 世纪                                                         | EXTRACT(CENTURY FROM TIMESTAMP '2000-12-16 12:21:13');    | 20       |
| DAY          | (月分)里的日期域(1-31)                                       | EXTRACT(DAY from TIMESTAMP '2001-02-16 20:38:40');        | 16       |
| DECADE       | 年份域除以10                                                 | EXTRACT(DECADE from TIMESTAMP '2001-02-16 20:38:40');     | 200      |
| DOW          | 每周的星期号(0-6；星期天是0) (仅用于timestamp)               | EXTRACT(DOW FROM TIMESTAMP '2001-02-16 20:38:40');        | 5        |
| DOY          | 一年的第几天(1 -365/366) (仅用于 timestamp)                  | EXTRACT(DOY from TIMESTAMP '2001-02-16 20:38:40');        | 47       |
| HOUR         | 小时域(0-23)                                                 | EXTRACT(HOUR from TIMESTAMP '2001-02-16 20:38:40');       | 20       |
| MICROSECONDS | 秒域，包括小数部分，乘以 1,000,000。                         | EXTRACT(MICROSECONDS from TIME '17:12:28.5');             | 28500000 |
| MILLENNIUM   | 千年                                                         | EXTRACT(MILLENNIUM from TIMESTAMP '2001-02-16 20:38:40'); | 3        |
| MILLISECONDS | 秒域，包括小数部分，乘以 1000。                              | EXTRACT(MILLISECONDS from TIME '17:12:28.5');             | 28500    |
| MINUTE       | 分钟域(0-59)                                                 | EXTRACT(MINUTE from TIMESTAMP '2001-02-16 20:38:40');     | 38       |
| MONTH        | 对于timestamp数值，它是一年里的月份数(1-12)；对于interval数值，它是月的数目，然后对12取模(0-11) | EXTRACT(MONTH from TIMESTAMP '2001-02-16 20:38:40');      | 2        |
| QUARTER      | 该天所在的该年的季度(1-4)(仅用于 timestamp)                  | EXTRACT(QUARTER from TIMESTAMP '2001-02-16 20:38:40');    | 1        |
| SECOND       | 秒域，包括小数部分(0-59[1])                                  | EXTRACT(SECOND from TIMESTAMP '2001-02-16 20:38:40');     | 40       |
| WEEK         | 该天在所在的年份里是第几周。                                 | EXTRACT(WEEK from TIMESTAMP '2001-02-16 20:38:40');       | 7        |
| YEAR         | 年份域                                                       | EXTRACT(YEAR from TIMESTAMP '2001-02-16 20:38:40');       | 2001     |



# 十三、Citus分布表

先创建一张普通的表

```plsql
create table aa_test(
  name int8
)

--第一种方式，可用于非空表
show citus.shard_count;
show citus.shard_replication_factor;
select create_distributed_table('test','id','hash');

--第二种方式，只能是空表
select master_create_distributed_table('test','id','hash');
select master_create_worker_shards('test',2,1);


select * from pg_dist_partition;
select * from pg_dist_shard;
select * from pg_dist_colocation;
select * from pg_dist_local_group;
select * from pg_dist_node;
select * from pg_dist_node_metadata;
select * from pg_dist_placement;
select * from pg_dist_poolinfo;
select * from pg_dist_transaction;
select * from pg_dist_rebalance_strategy;
select * from pg_dist_shard_placement;
```



例子：

```plsql
create table test(id integer);

--第一种方式，6个分片，1个副本
show citus.shard_count;
show citus.shard_replication_factor;
set citus.shard_count=6;  --6个分片
set citus.shard_replication_factor=1;  --1个复制
select create_distributed_table('test','id','hash');  --创建分布表，自动获取citus.shard_count和citus.shard_replication_factor生产相应的分片和副本

insert into test select generate_series(1,100);

select * from pg_dist_shard;
```



```plsql
create table test1(id integer);

--第二种方式
select master_create_distributed_table('test1','id','hash');
select master_create_worker_shards('test1',10,2);  --10分片，2副本

insert into test1 select generate_series(1,100);
```



# 十四、锁表

```plsql
--查看被锁的表
select * from pg_locks

--kill进程
select pg_terminate_backend(pid); 
select pg_cancle_backend(pid); 
```



# 十四、使用密码文件

一个用户主目录中的`.pgpass`文件能够包含在连接需要时使用的口令（并且其他情况不会指定口令）。在微软的 Windows 上该文件被命名为`%APPDATA%\postgresql\pgpass.conf`（其中`%APPDATA%`指的是用户配置中的应用数据子目录）。另外，可以使用连接参数[passfile](http://postgres.cn/docs/11/libpq-connect.html#LIBPQ-CONNECT-PASSFILE)或者环境变量`PGPASSFILE`指定一个口令文件。

这个文件应该包含下列格式的行：

```
hostname:port:database:username:password
```

（你可以向该文件增加一个提醒：把上面的行复制到该文件并且在前面加上`#`）。前四个域的每一个都可以是文字值或者匹配任何东西的`*`。第一个匹配当前连接参数的行中的口令域将被使用（因此，在使用通配符时把更特殊的项放在前面）。如果一个条目需要包含`:`或者`\`，用`\`对该字符转义。如果指定了`host`连接参数，主机名字段会被匹配到`host`，否则如果指定了`hostaddr`参数则匹配到`hostaddr`，如果两者都没有给出，则会搜索主机名`localhost`。当连接是一个Unix域套接字连接并且`host`参数匹配libpq的默认套接字目录路径时，也会搜索主机名`localhost`。在一台后备服务器上，值为`replication`的数据库字段匹配连接到主服务器的里复制连接。否则数据库字段的用途有限，因为用户对同一个集簇中的所有数据库都有相同的口令。

在 Unix 系统上，口令文件上的权限必须不允许所有人或组内访问，可以用`chmod 0600 ~/.pgpass`这样的命令实现。如果权限没有这么严格，该文件将被忽略。在微软 Windows 上，该文件被假定存储在一个安全的目录中，因此不会进行特别的权限检查。

```sql
# hostname:port:database:username:password

132.108.212.128:5433:jsdb:bss_gz:ZuseP*NFye86
132.121.1.74:5553:jsdb:bss_gz:ZuseP*NFye86
132.121.1.73:5523:jsdb:bss_gz:ZuseP*NFye86
132.121.1.75:5573:jsdb:bss_gz:ZuseP*NFye86
132.121.1.68:5433:jsdb:bss_gz:ZuseP*NFye86
132.121.1.70:5493:jsdb:bss_gz:ZuseP*NFye86
132.121.1.69:5463:jsdb:bss_gz:ZuseP*NFye86
```





# 十五、使用service

连接服务文件允许 libpq 连接参数与一个单一服务名称关联。那个服务名称可以被一个 libpq 连接指定，与其相关的设置将被使用。这允许在不重新编译 libpq 应用的前提下修改连接参数。服务名称也可以被使用`PGSERVICE`环境变量来指定。

连接服务文件可以是每个用户都有一个的服务文件，它位于`~/.pg_service.conf`或者环境变量`PGSERVICEFILE`指定的位置。它也可以是一个系统范围的文件，位于``pg_config --sysconfdir`/pg_service.conf`的或者环境变量`PGSYSCONFDIR`指定的目录。如果相同名称的服务定义存在于用户和系统文件中，用户文件将优先考虑。

```sql
# CN节点
[cn]
host=132.108.212.128
port=5433
dbname=jsdb
user=bss_gz
password=ZuseP*NFye86
keepalives_idle=60	# 连接保持

# worker1节点
[worker1]
host=132.121.1.74
port=5553
dbname=jsdb
user=bss_gz
password=ZuseP*NFye86
keepalives_idle=60	# 连接保持
```



# 十六、for...in...loop...循环

需要定义接收变量

```sql
do language plpgsql $$
declare
  rec record;
begin
  for rec in (select * from test1) loop
    raise notice '%',rec.id;
  end loop;
end;
$$;
```



# 十七、pgAgent 定时器

启动pgagent，可以启动多个

```
pgagent hostaddr=127.0.0.1 port=5432 dbname=stock user=stock password=stock
```



```plsql
select * from pgagent.pga_job

select * from pgagent.pga_jobagent

select * from pgagent.pga_joblog

select * from pgagent.pga_jobclass

select * from pgagent.pga_jobstep

select * from pgagent.pga_jobsteplog

select * from pgagent.pga_schedule

select * from pgagent.pga_exception
```

创建定时任务

```plsql
DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
		-- Creating a new job
		INSERT INTO pgagent.pga_job(
				jobjclid, jobname, jobdesc, jobhostagent, jobenabled
		) VALUES (
				1::integer, 'aa'::text, ''::text, ''::text, true
		) RETURNING jobid INTO jid;

		-- Steps
		-- Inserting a step (jobid: NULL)
		INSERT INTO pgagent.pga_jobstep (
				jstjobid, jstname, jstenabled, jstkind,
				jstconnstr, jstdbname, jstonerror,
				jstcode, jstdesc
		) VALUES (
				jid, 'aa'::text, true, 's'::character(1),
				'host=127.0.0.1 port=5432 dbname=orig user=orig password=orig'::text, ''::name, 'f'::character(1),
				'select 1;'::text, ''::text
		) ;-- Inserting a step (jobid: NULL)
		INSERT INTO pgagent.pga_jobstep (
				jstjobid, jstname, jstenabled, jstkind,
				jstconnstr, jstdbname, jstonerror,
				jstcode, jstdesc
		) VALUES (
				jid, 'bb'::text, true, 's'::character(1),
				''::text, 'orig'::name, 'f'::character(1),
				'select 2;'::text, ''::text
		) ;

		-- Schedules
		-- Inserting a schedule
		INSERT INTO pgagent.pga_schedule(
				jscjobid, jscname, jscdesc, jscenabled,
				jscstart, jscend,    jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
		) VALUES (
				jid, 'aa'::text, ''::text, true,
				'2020-11-19T15:57:58+08:00'::timestamp with time zone, '2020-11-26T15:58:00+08:00'::timestamp with time zone,
				-- Minutes，00-59
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Hours，00-23
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Week days，星期天-星期六
				ARRAY[false,false,false,false,false,false,false]::boolean[],
				-- Month days，00-31，月最后一天
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Months，01-12
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false]::boolean[]
		) RETURNING jscid INTO scid;-- Inserting a schedule
		INSERT INTO pgagent.pga_schedule(
				jscjobid, jscname, jscdesc, jscenabled,
				jscstart, jscend,    jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
		) VALUES (
				jid, 'bb'::text, ''::text, true,
				'2020-11-19 07:58:07 +00:00'::timestamp with time zone, '2020-11-20 07:58:08 +00:00'::timestamp with time zone,
				-- Minutes
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Hours
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Week days
				ARRAY[false,false,false,false,false,false,false]::boolean[],
				-- Month days
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
				-- Months
				ARRAY[false,false,false,false,false,false,false,false,false,false,false,false]::boolean[]
		) RETURNING jscid INTO scid;
END
$$;
```



# 十八、PostgreSQL的PL/pgSQL语言和 Oracle 的PL/SQL语言之间的差别

http://postgres.cn/docs/11/plpgsql-porting.html



# 十九、upsert

```sql
--on conflict
insert into blog as a
select * from blog1 b
on conflict (id) do  --id是主键或唯一键
update 
  set title='2'
  
--先更新，后插入
with upsert as (
    update blog tt
    set title=b.title
    from blog1 b
    where tt.id=b.id
    returning tt.*)

insert into blog
select * from blog1 t1
where not exists (select 1 from upsert t2 where t1.id=t2.id)
```

# 二十、查看表字段

```sql
select * from information_schema.columns
where table_schema='etl' 
and table_name='tmp_stock_basic'
order by ordinal_position;
```

# 二十一、查看函数或存储过程的定义

```sql
select pg_get_functiondef('etl.pro_inc_namechange'::regproc);


select p.oid,
	p.proname "函数名",
	format('%I.%I(%s)', ns.nspname, p.proname, oidvectortypes(p.proargtypes)) "函数全名",
	p.oid::regprocedure "函数全名",
	prorettype::regtype "返回值类型"
	--pg_get_functiondef(p.oid) "函数定义"
from pg_proc p
	join pg_namespace ns on p.pronamespace = ns.oid
where p.proname = 'pro_inc_namechange';
```

# 二十二、jsonb转表

```sql
select *
from pg_catalog.jsonb_to_recordset(
	(select api_in_param
	from stock.tbl_global_config
	where id = 2
	limit 1
	)
) as t(
	名称 text, 
	描述 text, 
	类型 text, 
	必选 text
);
```

# 二十三、plpgsql块

```sql
DO LANGUAGE plpgsql
$$ 
BEGIN
	RAISE NOTICE '1234';
END;
$$;
```

# 二十四、plpython3u块

```python
DO $$
    import pandas as pd
    plpy.notice('hello')
$$ LANGUAGE plpython3u;
```

# 二十五、CentOS安装pgAgent

```shell
# 安装源
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm 

yum install pgagent_12

# 创建 schema pgagent 
stock => \i /usr/share/pgagent_12-4.0.0/pgagent.sql
# 启动 pgagent，参数与上面创建的schema对应
pgagent_12 hostaddr=127.0.0.1 port=5432 dbname=stock user=stock password=stock.orig.xin

```



# 二十六、CentOS安装pgAdmin

```shell
virtualenv /opt/pgAdmin --python /usr/bin/python3

. /opt/pgAdmin/bin/activate

pip install pgadmin4

# 创建配置文件
vim /opt/pgAdmin4/lib/python3.6/site-packages/pgadmin4/config_local.py

LOG_FILE = '/opt/pgAdmin4/log/pgadmin4.log'
SQLITE_PATH = '/opt/pgAdmin4/pgadmin4.db'
SESSION_DB_PATH = '/opt/pgAdmin4/sessions'
STORAGE_DIR = '/opt/pgAdmin4/storage'
DEFAULT_SERVER = '0.0.0.0'
DEFAULT_SERVER_PORT = 5050

# 创建 pgadmin4.services

[Unit]
Description=jupyter
After=network.target

[Service]
User=postgres
Group=postgres
Type=simple
# ExecStartPre=
ExecStart=/opt/pgAdmin4/bin/pgadmin4
# ExecReload=
# ExecStop=

PrivateTmp=True

[Install]
WantedBy=multi-user.target



# 刷新systemd配置
systemctl daemon-reload

systemctl start pgadmin4
```



# 二十六、查看表的膨胀率

```sql
select relid,
	schemaname,
	relname as tablename, 
	pg_size_pretty(pg_relation_size(relid)) as table_size, 
	n_dead_tup, 
	n_live_tup,
	case when n_live_tup + n_dead_tup = 0 then 0 else round(n_dead_tup * 100 / (n_live_tup + n_dead_tup), 2) end as "dead_tup_ratio(%)",  --表膨胀率
	greatest(last_vacuum,last_autovacuum) as last_vacuum_time,
	greatest(last_analyze,last_autoanalyze) as last_analyze_time
from pg_stat_all_tables  --pg_stat_user_tables
where schemaname <> 'pg_catalog'
and schemaname <> 'information_schema'
and schemaname !~ '^pg_toast'
order by "dead_tup_ratio(%)" desc;
```



