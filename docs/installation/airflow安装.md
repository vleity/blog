[@id]: 20210906-01.md
[@title]: 安装Airflow任务调度平台
[@location]: docs/installation/20210906-01.md
[@author]: leity
[@date]: 2021-09-06

## 文章标题

#### 作者

leity

#### 日期

2021-09-06

#### 标签

PostgreSql ，数据库

------

## 背景

## 二级标题

### 三级标题

#### 四级标题

##### 五级标题

###### 六级标题

## 二级标题



```shell
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=/home/leo/airflow/airflow

AIRFLOW_VERSION=2.1.3
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.1.3/constraints-3.6.txt
pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email vleity@163.com

# start the web server, default port is 8080
airflow webserver --port 8080

# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page
```

