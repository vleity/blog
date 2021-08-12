# CentOS 7 源码安装 LNMP 之 Nginx 1.18.0

> `Nginx("engine x")`是一款是由俄罗斯的程序设计师 `cIgor Sysoevc` 所开发高性能的 `Web` 和反向代理服务器，也是一个 `IMAP/POP3/SMTP` 代理服务器。在高连接并发的情况下， `Nginx` 是 `Apache` 服务器不错的替代品。

> 下载地址：`http://nginx.org/download/nginx-1.18.0.tar.gz`

## 下载源码包

```
[root@localhost Downloads]# wget http://nginx.org/download/nginx-1.18.0.tar.gz
```

## 安装编译工具及库文件

```
[root@localhost Downloads]# yum install make automake autoconf libtool gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel 
```

## 创建 www 用户

```
[root@localhost Downloads]# useradd -s /sbin/nologin www
```

## 解压nginx源码包并编译安装

```
[root@localhost Downloads]# tar -zxvf nginx-1.18.0.tar.gz
[root@localhost Downloads]# cd nginx-1.18.0
[root@localhost nginx-1.18.0]# ./configure --prefix=/opt/nginx
...
[root@localhost nginx-1.18.0]# make && make install
...
```

## 修改配置文件 conf/nginx.conf

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
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

## 配置 systemd

```
[root@localhost nginx]# vim /usr/lib/systemd/system/nginx.service
```

`nginx.service`

```bash
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/opt/nginx/logs/nginx.pid
ExecStartPre=/opt/nginx/sbin/nginx -t
ExecStart=/opt/nginx/sbin/nginx
ExecReload=/opt/nginx/sbin/nginx -s reload
ExecStop=/usr/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

重载服务配置

```
[root@localhost nginx]# systemctl daemon-reload
```

开机自动启动

```
[root@localhost nginx]# systemctl enable nginx
```

启动服务

```
[root@localhost nginx]# systemctl start nginx
```

浏览器访问 http://127.0.0.1:80 验证是否成功。
