# hana

# 一、查看表的字段

```plsql
select schema_name,table_name,column_name,DATA_TYPE_NAME
from sys.table_columns
where schema_name = 'MSS_BZPT_GD_P'
and table_name = 'ELECTRONIC_INVOICE_INFO'
and column_name in ('COMMODITY_NAME','PURCHASER_NAME','SALES_NAME')
```



# 二、查看对象的依赖关系

```plsql
--查看GD_V_ALL_DATA_MESSAGE_VIEW的底表
SELECT * FROM "SYS"."OBJECT_DEPENDENCIES"
WHERE DEPENDENT_SCHEMA_NAME = 'MSS_GUANGDONG'
AND DEPENDENT_OBJECT_NAME = 'GD_V_ALL_DATA_MESSAGE_VIEW';

--查看谁用了GD_V_ALL_DATA_MESSAGE_VIEW
SELECT * FROM "SYS"."OBJECT_DEPENDENCIES"
WHERE BASE_SCHEMA_NAME = 'MSS_GUANGDONG'
AND BASE_OBJECT_NAME = 'GD_V_ALL_DATA_MESSAGE_VIEW';
```



# 三、数据类型扩展

## 标量数据类型

| 数据类型     | 关键字                                                       |
| ------------ | ------------------------------------------------------------ |
| 数值类型     | TINYINT SMALLINT INT BIGINT DECIMAL SMALLDECIMAL REAL DOUBLE |
| 字符串类型   | VARCHAR NVARCHAR ALPHANUM                                    |
| 日期时间类型 | TIMESTAMP SECONDDATE DATE TIME                               |
| 二进制类型   | VARBINARY                                                    |
| 大对象类型   | CLOB NCLOB BLOB                                              |
| 空间类型     | ST_GEOMETRY                                                  |
| 布尔类型     | BOOLEAN                                                      |

*注：字符串类型 VARCHAR 和 NVARCHAR 最大支持存储 8388607个字符。*

## 表格类型

### 创建类型

```PLSQL
--创建类型语法
CREATE TYPE <type_name> AS TABLE (<column_list_definition>)
```

```PLsql
--举例创建表格类型 tt_publishers
CREATE TYPE tt_publishers AS TABLE (
publisher INTEGER,
name VARCHAR(50),
price DECIMAL,
cnt INTEGER);
```

### 删除类型

```PLSQL
--删除类型语法
DROP TYPE <type_name> [<drop_option>]
```

```PLsql
--举例删除表格类型 tt_publishers
DROP TYPE tt_publishers;
```

## 行类型变量

创建行类型

```PLSQL
DECLARE a ROW (a INT, b VARCHAR(16), c TIMESTAMP);
DECLARE b ROW LIKE <persistent table name>;
DECLARE c ROW LIKE :<other table/row/cursor variable name>;
```

给行类型变量赋值

```PLSQL
DO BEGIN
	--定义行类型变量x和y
    DECLARE x, y ROW (a INT, b VARCHAR(16), c TIMESTAMP);
    x = ROW(1, 'a', '2000-01-01');	--给x赋值
    x.a = 2;	--给x的a赋予2
    y = :x;	--将x赋值给y
    SELECT :y.a, :y.b, :y.c FROM DUMMY;
    -- Returns [2, 'a', '2000-01-01']
END;
```

SELECT 值到行类型变量

```PLSQL
DO BEGIN
	--定义游标
    DECLARE CURSOR cur FOR SELECT 1 as a, 'a' as b, to_timestamp('2000-01-01') as c FROM DUMMY;
    DECLARE x ROW LIKE :cur;
    OPEN cur;
    FETCH cur INTO x;
    SELECT :x.a, :x.b, :x.c FROM DUMMY;
    -- Returns [1, 'a', '2000-01-01']
    SELECT 2, 'b', '2000-02-02' INTO x FROM DUMMY;
    SELECT :x.a, :x.b, :x.c FROM DUMMY;
    -- Returns [2, 'b', '2000-02-02']
END;
```

- 在标量用户定义函数中不支持行类型变量
- 不支持 EXEC INTO
- 不能作为存储过程或函数的参数



# 四、存储过程

## 存储过程

### 创建存储过程

```PLSQL
CREATE [OR REPLACE] PROCEDURE <proc_name> [(<parameter_clause>)] [LANGUAGE <lang>] [SQL SECURITY <mode>] [DEFAULT SCHEMA <default_schema_name>]
    [READS SQL DATA ] [WITH ENCRYPTION] [AUTOCOMMIT DDL ON|OFF] AS
    BEGIN [SEQUENTIAL EXECUTION]
    <procedure_body>
END
```

例子：

```PLSQL
CREATE PROCEDURE orchestrationProc
LANGUAGE SQLSCRIPT AS
BEGIN
    DECLARE v_id BIGINT;
    DECLARE v_name VARCHAR(30);
    DECLARE v_pmnt BIGINT;
    DECLARE v_msg VARCHAR(200);
    DECLARE CURSOR c_cursor1 (p_payment BIGINT) FOR
    SELECT id, name, payment FROM control_tab
    WHERE payment > :p_payment ORDER BY id ASC;
    CALL init_proc();
    OPEN c_cursor1(250000);
    FETCH c_cursor1 INTO v_id, v_name, v_pmnt; v_msg = :v_name || ' (id ' || :v_id || ') earns ' || :v_pmnt || ' $.';
    CALL ins_msg_proc(:v_msg);
    CLOSE c_cursor1;
END;
```

### 删除存储过程

```plsql
DROP PROCEDURE <proc_name> [<drop_option>]
--<proc_name> ::= [<schema_name>.]<identifier>
--<drop_option> ::= CASCADE | RESTRICT
```

```PLSQL
DROP PROCEDURE my_proc
```

### 修改存储过程

```PLSQL
ALTER PROCEDURE <proc_name> [(<parameter_clause>)] [LANGUAGE <lang>]
[DEFAULT SCHEMA <default_schema_name>]
[READS SQL DATA] AS
BEGIN [SEQUENTIAL EXECUTION]
	<procedure_body>
END
```

例子：

```PLSQL
CREATE PROCEDURE GET_PROCEDURES(OUT procedures TABLE(schema_name NVARCHAR(256),
                                                     name NVARCHAR(256)
                                                    ))
AS
BEGIN
	procedures = SELECT schema_name AS schema_name, procedure_name AS name FROM PROCEDURES;
END;
```

```PLSQL
ALTER PROCEDURE GET_PROCEDURES( OUT procedures TABLE(schema_name NVARCHAR(256), 
                                                     name NVARCHAR(256)
                                                    ))
AS
BEGIN
	procedures = SELECT schema_name AS schema_name, procedure_name AS name FROM PROCEDURES WHERE IS_VALID = 'TRUE';
END;
```

### 重新编译存储过程

```PLSQL
ALTER PROCEDURE <proc_name> RECOMPILESyntax
```

### 调用存储过程

#### call

```PLSQL
CALL <proc_name> (<param_list>) [WITH OVERVIEW]
```

***WITH OVERVIEW 定义一个过程调用的结果直接将存储到一个物理表***

```PLSQL
CREATE PROCEDURE proc(
                    IN value integer,
    				IN currency nvarchar(10),
    				OUT outTable typeTable,
                    OUT valid integer)
AS
BEGIN
…
END;


--Calling the proc procedure:
CALL proc(1000, 'EUR', ?, ?);
--Calling the proc procedure using the WITH OVERVIEW option:
CALL proc(1000, 'EUR', ?, ?) WITH OVERVIEW;
--It is also possible to use scalar user defined function as parameters for procedure call:
CALL proc(udf(),’EUR’,?,?);
CALL proc(udf()* udf()-55,’EUR’, ?, ?);
```

#### 指定参数调用

```PLSQL
CALL myproc (i => 2)

call myproc(intab=>mytab, i=>2, outtab =>?);
--下面也是一样的，指定参数名，参数顺序可以不一样
call myproc( i=>2, intab=>mytab, outtab =>?)
```



**总结：**
1、创建的存储过程直接call调用报错，需要在calculate view中进行调用
2、calculate view的SQL script第一次出数据结果 script_view，semantics对script_view进行分组聚合
3、使用with result view ...时应注意：要有输出表参数，调用时参数名"$$<...>$$"必须要小写



### 存储过程参数

| 模式  | 描述         |
| ----- | ------------ |
| IN    | 输入参数     |
| OUT   | 输出参数     |
| INOUT | 输入输出参数 |

#### 调用带参存储过程

标量参数

```PLSQL
CREATE PROCEDURE test_scalar (IN i INT, IN a VARCHAR)
AS
BEGIN
	SELECT i AS "I", a AS "A" FROM DUMMY;
END;

--调用
CALL test_scalar (1, 'ABC');
CALL test_scalar (1+1, upper('abc'))
```

表格参数

```PLSQL
--创建表格类型
CREATE TYPE tab_type AS TABLE (I INT, A VARCHAR);
--创建表
CREATE TABLE tab1 (I INT, A VARCHAR);
--创建表格参数存储过程
CREATE PROCEDURE test_table (IN tab tab_type)
AS
BEGIN
	SELECT * FROM :tab;
END;

--调用，参数是一张表
CALL test_table (tab1);
CALL test_table ("tab1");	--表明区分大小写时加双引号
```

参数默认值

```PLSQL
IN <param_name> (<sql_type>|<table_type>|<table_type_definition>) DEFAULT (<value>|<table_name>)
```

```PLSQL
CREATE COLUMN TABLE NAMES(Firstname NVARCHAR(20), LastName NVARCHAR(20));
INSERT INTO NAMES VALUES('JOHN', 'DOE');
CREATE COLUMN TABLE MYNAMES(Firstname NVARCHAR(20), LastName NVARCHAR(20));
INSERT INTO MYNAMES VALUES('ALICE', 'DOE');
```

```PLSQL
CREATE PROCEDURE FULLNAME(
    IN INTAB TABLE(FirstName NVARCHAR (20), LastName NVARCHAR (20)) DEFAULT NAMES,
    IN delimiter VARCHAR(10) DEFAULT ', ',
    OUT outtab TABLE(fullname NVarchar(50))
)
AS
BEGIN
	outtab = SELECT lastname||:delimiter|| firstname AS FULLNAME FROM :intab;
END;
```

```PLSQL
CALL FULLNAME (outtab=>?);
--结果
FULLNAME
--------
DOE,JOHN

CALL FULLNAME(INTAB=> MYNAMES, outtab => ?)
--结果
FULLNAME
--------
DOE,ALICE
```

参数默认为空表

```PLSQL
(IN|OUT) <param_name> (<table_type>|<table_type_definition>) DEFAULT EMPTY
```

```PLSQL
CREATE PROCEDURE PROC_EMPTY (OUT OUTTAB TABLE(I INT) DEFAULT EMPTY)
AS
BEGIN

END;

--返回空表
call PROC_EMPTY (?);
```

```PLSQL
CREATE PROCEDURE CHECKINPUT (IN intab TABLE(I INT ) DEFAULT EMPTY,
                             OUT result NVARCHAR(20)
                             )
AS
BEGIN
    IF IS_EMPTY(:intab) THEN
    	result = 'Input is empty';
    ELSE
    	result = 'Input is not empty';
    END IF;
END;

--调用
call CHECKINPUT(result=>?)
--结果
OUT(1)
-----------------
'Input is empty'
```



# 五、自定义函数

## 创建函数

```PLSQL
CREATE [OR REPLACE] FUNCTION <func_name> [(<parameter_clause>)] RETURNS <return_type> [LANGUAGE <lang>] [SQL SECURITY <mode>][DEFAULT SCHEMA <default_schema_name> [DETERMINISTIC]]
[WITH ENCRYPTION]
AS
BEGIN
	<function_body>
END
```

例子

```PLSQL
CREATE FUNCTION scale (val INT)
RETURNS TABLE (a INT, b INT) 
LANGUAGE SQLSCRIPT AS
BEGIN
	RETURN SELECT a, :val * b AS b FROM mytab;
END;


--调用
SELECT * FROM scale(10);
SELECT * FROM scale(10) AS a, scale(10) AS b where a.a = b.a
```

返回多个值

```PLSQL
CREATE FUNCTION func_add_mul(x Double, y Double)
RETURNS result_add Double, result_mul Double
LANGUAGE SQLSCRIPT READS SQL DATA AS
BEGIN
    result_add = :x + :y;
    result_mul = :x * :y;
END;

CREATE TABLE TAB (a Double, b Double);
INSERT INTO TAB VALUES (1.0, 2.0);
INSERT INTO TAB VALUES (3.0, 4.0);
SELECT a, b, 
	func_add_mul(a, b).result_add as ADD, 
	func_add_mul(a, b).result_mul as MUL 
FROM TAB ORDER BY a;
--结果
A B ADD MUL
------------
1 2 3   2
3 4 7   12
```

## 修改函数

```PLSQL
ALTER FUNCTION <func_name> RETURNS <return_type> [LANGUAGE <lang>]
[DEFAULT SCHEMA <default_schema_name>]
AS
BEGIN
	<function_body>
END
```

例子

```PLSQL
CREATE FUNCTION GET_FUNCTIONS
returns TABLE(schema_name NVARCHAR(256),
			  name NVARCHAR(256))
AS
BEGIN
	return 
	SELECT schema_name AS schema_name,function_name AS name 
	FROM FUNCTIONS;
END;


ALTER FUNCTION GET_FUNCTIONS
returns TABLE(schema_name NVARCHAR(256),
			  name NVARCHAR(256))
AS
BEGIN
	return 
	SELECT schema_name AS schema_name,function_name AS name 
	FROM FUNCTIONS
	WHERE IS_VALID = 'TRUE';
END;
```

## 删除函数

```PLSQL
DROP FUNCTION <func_name> [CASCADE | RESTRICT]
--CASCADE:删除函数和依赖函数的对象
--RESTRICT:删除没有依赖于对象的函数，如果有对象依赖函数，则抛出错误
```



```plsql
SELECT
	 * 
FROM ( SELECT
	 ROW_NUMBER() OVER ( PARTITION BY A.POSID ORDER BY a.DATE_DO desc ) AS ROW_NUM,
	 DATE_DO,
	 DATE_PRE,
	 DATE_PRE1,
	 DATE_PRE2,
	 DATE_PRE3,
	 DATE_PRE4,
	 DATE_PRE5,
	 POSID 
	FROM "MSS_GD_PRD"."ZFIINT002" as a) 
WHERE ROW_NUM = '1'
```





```plsql
--复制表  WITH DATA 数据也复制，只复制表结构不加WITH DATA
CREATE TABLE NEWTABLE LIKE OLDTABLE WITH DATA;
```



# 六、将存储过程返回结果输出到一张视图

```PLSQL
--创建存储过程时使用 with result view view_name
create procedure PRC ( 
     IN  in_year varchar(4),
     IN  in_month varchar(2),
     IN  in_yszz  varchar(5000),
	 OUT OUT_PS_ZJGC_YS OUT_PS_ZJGC_YS
	 ) language sqlscript reads sql data 
	 with result view PRC
as
begin
	...
end;

--调用存储过程时使用 WITH OVERVIEW
call prc with overview table_name; --表要存在且表结构相似

select * 
from PRC
(
placeholder."$$in_year$$"=>:in_year,
placeholder."$$in_month$$"=>:in_month,
placeholder."$$in_yszz$$"=>:in_yszz
);

--------------------------------------------------------------------------------------
/*创建和调用
注意：必须有输出表变量，
*/
CREATE PROCEDURE MSS_GUANGDONG.PRO_LEITY02(IN DEPTNO DOUBLE,OUT RESULT "MSS_GUANGDONG"."V_TEST_EMP")
LANGUAGE SQLSCRIPT DEFAULT SCHEMA MSS_GUANGDONG READS SQL DATA WITH RESULT VIEW "MSS_GUANGDONG"."P_V_TEST_EMP"
AS
BEGIN
	RESULT = 
        SELECT * FROM "MSS_GUANGDONG"."TEST_EMP"
        WHERE DEPTNO = :DEPTNO;
END;

--调用

SELECT *
FROM "MSS_GUANGDONG"."P_V_TEST_EMP"
(
PLACEHOLDER."$$deptno$$"=>10	--"$$<parameter>$$"  必须小写
);

```



# 七、HANA时间函数

```PLSQL
--在日期基础上加上30天
SELECT ADD_DAYS(TO_DATE('2015-10-20','YYYY-MM-DD'),30) "add days" FROM DUMMY;
--在日期基础上加上1个月
SELECT ADD_MONTHS(TO_DATE('2015-10-20','YYYY-MM-DD'),1) "add months" FROM DUMMY;
--在时间基础上加上60*30秒
SELECT ADD_SECONDS(TO_TIMESTAMP('2015-10-21 23:30:45'),60*30) "add seconds" FROM DUMMY;
--在日期基础上加上1年
SELECT ADD_YEARS(TO_DATE('2009-12-05','YYYY-MM-DD'), 1) "add years" FROM DUMMY;
--返回当前的日期
SELECT CURRENT_DATE "current date" FROM DUMMY;
--返回当前的时间 日期+时间  精确到毫秒
SELECT CURRENT_TIMESTAMP "current timestamp" FROM DUMMY;
--返回该日期的英文星期几全拼  TUSEDAY
SELECT DAYNAME('2015-10-20') "dayname" FROM DUMMY;
--返回该日期在该月的第几天
SELECT DAYOFMONTH('2011-05-30') "dayofmonth" FROM DUMMY;
--返回该日期在该年的第几天
SELECT DAYOFYEAR('2011-05-30') "dayofyear" FROM DUMMY;
--返回两个日期之间相差的天数  前一个日期小于后一个日期，否则返回负数
SELECT DAYS_BETWEEN(TO_DATE('2009-12-05','YYYY-MM-DD'), TO_DATE('2010-01-05', 'YYYY-MM-DD')) "days between" FROM DUMMY;
--返回年份 数字形式
SELECT EXTRACT (YEAR FROM TO_DATE ('2010-01-04', 'YYYY-MM-DD')) "extract" FROM DUMMY;
--返回该日期时间的小时
SELECT HOUR ('2010-01-04 12:34:56') "hour" FROM DUMMY;
--返回该日期在该年处于第几周
SELECT ISOWEEK(TO_DATE('2011-05-30','YYYY-MM-DD')) "isoweek" FROM DUMMY;
--返回该日期所在月的最后一天
SELECT LAST_DAY (TO_DATE('2010-01-04', 'YYYY-MM-DD')) "last day" FROM DUMMY;
--返回该日期时间的分钟
SELECT MINUTE ('2010-01-04 12:34:56') "minute" FROM DUMMY;
--返回该日期的月份
SELECT MONTH ('2011-05-30') "month" FROM DUMMY;
--返回该日期的月份的英文全拼
SELECT MONTHNAME ('2011-10-30') "monthname" FROM DUMMY;
--返回该日期的下一天  =2009-12-31 + 1
SELECT NEXT_DAY (TO_DATE ('2009-12-31', 'YYYY-MM-DD')) "next day" FROM DUMMY;
--返回当前日期时间
SELECT NOW() "now" FROM DUMMY;
--返回该日期在该年度的第几个季度 4标识4月开始第一季度
SELECT QUARTER (TO_DATE('2015-04-01', 'YYYY-MM-DD'), 4) "quarter" FROM DUMMY;
--返回秒
SELECT SECOND ('2015-04-01 12:34:56') "second" FROM DUMMY;
--返回两个日期相差的秒数
SELECT SECONDS_BETWEEN ('2009-12-31', '2010-01-01') "seconds between" FROM DUMMY;
--返回该日期在该年中是第几个星期
SELECT WEEK (TO_DATE('2011-05-30', 'YYYY-MM-DD')) "week" FROM DUMMY;
--返回该日期在该星期中是第几天  返回范围0-6 Monday（0） Sunday（6）
SELECT WEEKDAY (TO_DATE ('2019-08-08', 'YYYY-MM-DD')) "week day" FROM DUMMY;
--返回该日期的年
SELECT YEAR (TO_DATE ('2011-05-30', 'YYYY-MM-DD')) "year" FROM DUMMY;
```



```plsql
--返回97对应的Unicode符号
select nchar(97) from dummy;
--它返回已传递字符串中子字符串的位置。
select LOCATE('abcd','a') from dummy;

--查看表
SELECT TABLE_NAME,COLUMN_NAME,COMMENTS,DATA_TYPE_NAME||
	'('||TO_VARCHAR(LENGTH)||MAP(TO_VARCHAR(IFNULL(SCALE,0)),'0','',','||TO_VARCHAR(IFNULL(SCALE,0)))||')' LENGTH
FROM "SYS"."TABLE_COLUMNS"
WHERE SCHEMA_NAME = 'MSS_GD_PRD'
AND TABLE_NAME = 'BSIK'
ORDER BY TABLE_NAME,COLUMN_NAME;
```



# 八、数组

```plsql
KM = UNNEST( :KMAR) WITH ORDINALITY AS("KMAR","SEQ");
```



# 九、变量赋值的三种方式

```PLSQL
DECLARE V_A VARCHAR(10);
V_A = '123';	--第一种 =赋值
V_A := '123';	--第二种 :=赋值
SELECT '123' INTO V_A FROM DUMMY;	--第三种 select ... into V_A    :V_A是错的
SELECT '123' INTO :V_A FROM DUMMY;  --错误
SELECT V_A AS A FROM DUMMY;
SELECT :V_A AS A FROM DUMMY;
```

# 十、导出数据到文件

```
hdbsql -n 10.140.9.193:30015 -u MSS_GUANGDONG -p Init2016 -I E:\Auto_process\hana_table_report\report.sql -o E:\Auto_process\hana_table_report\table_report.txt
```



