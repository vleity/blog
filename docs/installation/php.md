下载：`https://www.php.net/distributions/php-7.2.31.tar.gz`

## 下载 php 源码包

```
[root@localhost Downloads]# wget https://www.php.net/distributions/php-7.2.31.tar.gz
```

## 安装依赖包

```
[root@localhost Downloads]# yum install gcc gcc-c++ zlib-devel zlib libxml-devel libxml2 libxslt-devel libxslt openssl openssl-devel libjpeg libjpeg-devel libpng ibpng-devel freetype freetype-devel gmp-devel curl libcurl libcurl-devel
```

## 解压 php 源码包并编译安装

```
[root@localhost Downloads]# tar -zxvf php-7.2.31.tar.gz
[root@localhost Downloads]# cd php-7.2.31/
[root@localhost php-7.2.31]# ./configure --prefix=/opt/php/php72 --with-config-file-path=/opt/php/php72/etc --enable-fpm --enable-mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --enable-zip --enable-mbstring --with-gd --with-zlib --with-curl --with-openssl --enable-pcntl
...
[root@localhost php-7.2.31]# make && make install
...
[root@localhost php-7.2.31]# cp php.ini-production /opt/php/php72/etc/php.ini
```

## 配置 php.ini

```
[root@localhost php-7.2.31]# cd /opt/php/php72/
[root@localhost php72]# vim etc/php.ini
```

`php.ini`

```
memory_limit = 1024M
cgi.fix_pathinfo=0
upload_max_filesize = 10240M
```

## 配置 php-fpm

```
[root@localhost php72]# cp etc/php-fpm.conf.default etc/php-fpm.conf
[root@localhost php72]# vim etc/php-fpm.conf
```

`php-fpm.conf`

```
pid = /opt/php/php72/var/run/php-fpm.pid
```

配置 `php-fpm.d/www.conf`

```
[root@localhost php72]# cp etc/php-fpm.d/www.conf.default etc/php-fpm.d/www.conf
[root@localhost php72]# vim etc/php-fpm.d/www.conf
```

`www.conf`

```
user = www
group = www
```

## 启动php-fpm

```
[root@localhost php72]# sbin/php-fpm
```

## 配置 nginx 支持 php

```
[root@localhost php72]# vim /opt/nginx/conf/nginx.conf
```

`nginx.conf `

```bash
user  www;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  localhost;
        location / {
            root   html;
            index  index.php index.html index.htm;
        }
        location ~* \.php$ {
            fastcgi_index   index.php;
            fastcgi_pass    127.0.0.1:9000;
            include         fastcgi_params;
            fastcgi_param   SCRIPT_FILENAME    $document_root$fastcgi_script_name;
            fastcgi_param   SCRIPT_NAME        $fastcgi_script_name;
        }   
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }   
    }   
}

```

重启 `nginx`

```
[root@localhost php72]# systemctl restart nginx
```

## 测试

`index.php`

```php
<?php
    phpinfo();
?>
```

浏览器访问 http://127.0.0.1

## systemd 管理 php-fpm

```
[root@localhost php72]# vim /usr/lib/systemd/system/php-fpm.service
```

`php-fpm.service`

```
[Unit]
Description=The PHP FastCGI Process Manager
After=syslog.target network.target

[Service]
Type=forking
PIDFile=/opt/php/php72/var/run/php-fpm.pid
ExecStart=/opt/php/php72/sbin/php-fpm
ExecStop=/usr/bin/kill -INT $MAINPID
ExecReload=/usr/bin/kill -USR2 $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

重载服务配置

```
[root@localhost php72]# systemctl daemon-reload
```

开机自动启动

```
[root@localhost php72]# systemctl enable php-fpm
```

启动服务

```
[root@localhost php72]# systemctl start php-fpm
```

